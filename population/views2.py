from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Population,Geojson,ColorRange,ColorRangeFamily
from .forms import StateSelectionForm,ColorRangeForm,ColorRangeFamilyForm
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models import Q


def add_color_family(request):
    if request.method == 'POST':
        form = ColorRangeFamilyForm(request.POST)
        if form.is_valid():
            color_range_family = form.save(commit=False)
            color_range_family.created_by = request.user
            color_range_family.save()
            return JsonResponse({'success':True,
                                 'new_family':{
                                     'family_name':color_range_family.family_name,
                                     'family_id':color_range_family.id,
                                     'delete_url': f'/delete-family/{color_range_family.id}/',
                                     'get_ranges_url':f'/get_color_ranges/{color_range_family.id}/'
                                  }})

def add_color_range(request):
    if request.method == 'POST':
        form = ColorRangeForm(request.POST)
        if form.is_valid():
            color_range = form.save(commit=False)
            color_family = ColorRangeFamily.objects.get(id=form.data.get('activeFamilyId'))
            color_range.color_range_family = color_family
            color_range.save()
            color_ranges = ColorRange.objects.filter(color_range_family=color_family)
            data = list(color_ranges.values())
            print(data)
            return JsonResponse({'success':True,'color_ranges':data}, safe=False)


def delete_color_family(request,pk):
    family = get_object_or_404(ColorRangeFamily, id=pk, created_by=request.user)
    family.delete()
    return JsonResponse({'success': True})

def delete_color_range(request,pk):
    color = ColorRange.objects.get(id=pk)
    color.delete()
    return JsonResponse({'success': True})


def add_json_color_range():
    data = json.load(open('/home/abhishek/Downloads/mapsofbharat/color_range_default.json','r'))
    for item in data:
        ColorRange.objects.create(
            start = item['start'],
            end = item['end'],
            color = item['color'],
            color_range_family = ColorRangeFamily.objects.get(id=1)
        )
# add_json_color_range()


def get_color(_sum,family_id):
    color_range_family = ColorRangeFamily.objects.get(id=family_id)
    color_range = ColorRange.objects.filter(
        color_range_family=color_range_family,
        start__lte=_sum,
        end__gte=_sum
    ).first()
    if color_range:
        return color_range.color, f'{color_range.start} - {color_range.end}'
    return 'gray','range not exists'



def get_population(request):
    try:
        data = json.loads(request.body)
        dataFilteringFields = data.get("dataFilteringFields", {})
        extraFields = data.get("extraFields", {})
        family_id = data.get("family_id")

        # ✅ Step 1: Get color ranges in bulk (NO Loop)
        color_range_family = ColorRangeFamily.objects.get(id=family_id)
        color_ranges = ColorRange.objects.filter(color_range_family=color_range_family)

        # ✅ Step 2: Pre-map the color ranges (NO Database Calls in Loop)
        color_map = {
            (cr.start, cr.end): (cr.color, f'{cr.start} - {cr.end}')
            for cr in color_ranges
        }

        # ✅ Step 3: Fetch Population Data (Single Query)
        filtered_data = (
            Population.objects
            .filter(**dataFilteringFields)
            .values(*extraFields)
            .annotate(population_sum=Sum("population"))
        )

        # ✅ Step 4: Process Data (0 Database Calls in Loop)
        response_data = {}
        for entry in filtered_data:
            # Find the color without hitting the database
            _sum = entry["population_sum"]
            color, value_range = 'gray', 'range not exists'
            for (start, end), (clr, rng) in color_map.items():
                if start <= _sum <= end:
                    color, value_range = clr, rng
                    break

            # Build the response
            key = '|'.join([str(entry[k]) for k in extraFields])
            response_data[key] = {
                **entry,
                "color": color,
                "value_range": value_range
            }
        print(response_data)

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)



def get_districts(request):
    state = request.GET.get('state')
    geojson = Geojson.objects.filter(state_name=state).first()
    with geojson.district_geojson.open('r') as file:
        geojson_data = json.load(file)
    districts = [feature['properties']['DIST_NAME'] for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower())]
    unique_districts = list(set(districts))
    return JsonResponse({'districts': unique_districts})


def get_sub_districts(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    geojson = Geojson.objects.filter(state_name=state).first()
    with geojson.sub_district_geojson.open('r') as file:
        geojson_data = json.load(file)
    sub_districts = [feature['properties']['SUB_DIST_N']  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower())]
    unique_sub_districts = list(set(sub_districts))
    return JsonResponse({'sub_districts': unique_sub_districts})

def get_blocks(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    sub_district = request.GET.get('sub_district')
    geojson = Geojson.objects.filter(state_name=state).first()
    with geojson.block_geojson.open('r') as file:
        geojson_data = json.load(file)
    blocks = [feature['properties']['BLOCK_NAME']  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower())]
    unique_blocks = list(set(blocks))
    return JsonResponse({'blocks': unique_blocks})

def get_pincodes(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    sub_district = request.GET.get('sub_district')
    block = request.GET.get('block')
    geojson = Geojson.objects.filter(state_name=state).first()
    with geojson.pincode_geojson.open('r') as file:
        geojson_data = json.load(file)
    pincodes = [feature['properties']['PINCODE']  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower()) and (feature['properties']['BLOCK_NAME'].lower()==block.lower())]
    unique_pincodes = list(set(pincodes))
    return JsonResponse({'pincodes': unique_pincodes})

def get_gram_panchayats(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    sub_district = request.GET.get('sub_district')
    block = request.GET.get('block')
    pincode = request.GET.get('pincode')
    geojson = Geojson.objects.filter(state_name=state).first()
    with geojson.gram_panchayat_geojson.open('r') as file:
        geojson_data = json.load(file)
    gram_panchayats = [feature['properties']['GP_NAME']  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower()) and (feature['properties']['BLOCK_NAME'].lower()==block.lower()) and (feature['properties']['PINCODE'].lower()==pincode.lower())]
    unique_gram_panchayats = list(set(gram_panchayats))
    return JsonResponse({'gram_panchayats': unique_gram_panchayats})

def get_town_villages(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    sub_district = request.GET.get('sub_district')
    block = request.GET.get('block')
    pincode = request.GET.get('pincode')
    gram_panchayat = request.GET.get('gram_panchayat')
    geojson = Geojson.objects.filter(state_name=state).first()
    with geojson.town_village_geojson.open('r') as file:
        geojson_data = json.load(file)
    town_villages = [feature['properties']['GP_NAME']  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower()) and (feature['properties']['BLOCK_NAME'].lower()==block.lower()) and (feature['properties']['PINCODE'].lower()==pincode.lower()) and (feature['properties']['GP_NAME'].lower()==gram_panchayat.lower())]
    unique_town_villages = list(set(town_villages))
    return JsonResponse({'town_villages': unique_town_villages})

def get_aplicable_boundaries(request):
    recently_changed_field = request.GET.get('recently_changed_field')
    status = request.GET.get('status')
    field_boundaries = {
        "state" : {'nonempty':['State Boundary','District Boundary','Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                   'empty':[]},
        "district" : {'nonempty':['District Boundary','Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                      'empty':['State Boundary','District Boundary','Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary']},
        "sub_district" : {'nonempty':['Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                          'empty':['District Boundary','Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary']},
        "block" : {'nonempty':['Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                   'empty':['Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary']},
        "pincode" : {'nonempty':['Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                     'empty':['Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary']},
        "gram_panchayat" : {'nonempty':['Grampanchayat Boundary','Town/Village Boundary'],
                            'empty':['Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary']},
        "town_village" : {'nonempty':['Town/Village Boundary'],
                          'empty':['Grampanchayat Boundary','Town/Village Boundary']},
    }
    return JsonResponse({'applicable_boundaries': field_boundaries[recently_changed_field][status]})


def get_data_filtering_fields(request):
    fields = {
        'state': request.POST.get('state'),
        'district': request.POST.get('district'),
        'sub_district': request.POST.get('sub_district'),
        'block': request.POST.get('block'),
        'pincode': request.POST.get('pincode'),
        'gram_panchayat': request.POST.get('gram_panchayat'),
        'town_village': request.POST.get('town_village')
    }
    filtered_fields = {k: v for k, v in fields.items() if v}
    return filtered_fields

def get_boundary_filtering_fields(request):
    fields = {
        'STATE_NAME': request.POST.get('state'),
        'DIST_NAME': request.POST.get('district'),
        'SUB_DIST_N': request.POST.get('sub_district'),
        'BLOCK_NAME': request.POST.get('block'),
        'PINCODE': request.POST.get('pincode'),
        'GP_NAME': request.POST.get('gram_panchayat'),
        'NAME': request.POST.get('town_village')
    }
    filtered_fields = {k: v for k, v in fields.items() if v}
    return filtered_fields


def get_geojson_url(request):
    state = request.POST.get('state')
    boundary = request.POST.get('boundary')
    geojson = Geojson.objects.get(state_name=state)
    boundary_vs_geojson_url = {
        'State Boundary': geojson.state_geojson.url,
        'District Boundary': geojson.district_geojson.url,
        'Sub-District Boundary': geojson.sub_district_geojson.url,
        'Block Boundary' : geojson.block_geojson.url,
        'Pincode Boundary': geojson.pincode_geojson.url,
        'Grampanchayat Boundary' : geojson.gram_panchayat_geojson.url,
        'Town/Village Boundary': geojson.town_village_geojson.url
    }
    return boundary_vs_geojson_url[boundary]

def get_last_nonempty_field(request):
    fields = {
        'state': request.POST.get('state'),
        'district': request.POST.get('district'),
        'sub_district': request.POST.get('sub_district'),
        'block': request.POST.get('block'),
        'town_village': request.POST.get('town_village'),
        'pincode': request.POST.get('pincode'),
        'gram_panchayat': request.POST.get('gram_panchayat')
    }
    for k, v in reversed(fields.items()):
        if v:
            return k


def get_form_object(request):
    if request.method == 'POST':
        form = StateSelectionForm(
            request.POST,
            state = request.POST.get('state'),
            district = request.POST.get('district'),
            sub_district = request.POST.get('sub_district'),
            block = request.POST.get('block'),
            town_village = request.POST.get('town_village'),
            pincode = request.POST.get('pincode'),
            gram_panchayat = request.POST.get('gram_panchayat'),
            last_nonempty_field = get_last_nonempty_field(request),
            user=request.user
        )
    else:
        form = StateSelectionForm(user=request.user)
    return form


def get_color_families(request):
    color_families = ColorRangeFamily.objects.filter(created_by=request.user)
    data = list(color_families.values())
    print(data)
    return JsonResponse({'success':True,'color_families':data}, safe=False)

def get_color_ranges(request,family_id):
    color_family = ColorRangeFamily.objects.get(id=family_id)
    color_ranges = ColorRange.objects.filter(color_range_family=color_family)
    data = list(color_ranges.values())
    print(data)
    return JsonResponse({'success':True,'color_ranges':data}, safe=False)

def get_extra_fields(request):
    boundary = request.POST.get('boundary')
    boundary_name_vs_extra_fields = {
        'State Boundary': {'state':'STATE_NAME'},
        'District Boundary': {'state':'STATE_NAME','district':'DIST_NAME'},
        'Sub-District Boundary': {'state':'STATE_NAME','district':'DIST_NAME','sub_district':'SUB_DIST_N'},
        'Block Boundary':{'state':'STATE_NAME','district':'DIST_NAME','sub_district':'SUB_DIST_N','block':'BLOCK_NAME'},
        'Pincode Boundary':{'state':'STATE_NAME','district':'DIST_NAME','sub_district':'SUB_DIST_N','block':'BLOCK_NAME','pincode':'PINCODE'},
        'Grampanchayat Boundary':{'state':'STATE_NAME','district':'DIST_NAME','sub_district':'SUB_DIST_N','block':'BLOCK_NAME','pincode':'PINCODE','gram_panchayat':'GP_NAME'},
        'Town/Village Boundary':{'state':'STATE_NAME','district':'DIST_NAME','sub_district':'SUB_DIST_N','block':'BLOCK_NAME','pincode':'PINCODE','gram_panchayat':'GP_NAME','town_village':'NAME'}
    }
    return boundary_name_vs_extra_fields[boundary]

def index(request):
    form = get_form_object(request)
    crf_form = ColorRangeFamilyForm()
    cr_form = ColorRangeForm()

    context = {
        'form': form,
        'crf_form':crf_form,
        'cr_form':cr_form,
    }
    if request.method == 'POST':
        geojson_url = get_geojson_url(request)
        boundary_filtering_fields = get_boundary_filtering_fields(request)
        data_filtering_fields = get_data_filtering_fields(request)
        extra_fields = get_extra_fields(request)

        context['geojson_url'] = geojson_url
        context['boundary_filtering_fields'] = boundary_filtering_fields
        context['data_filtering_fields'] = data_filtering_fields
        context['extra_fields'] = extra_fields 
        context['family_name'] = request.POST.get('family_name')
    return render(request, 'population/index.html', context)




import os
import shutil
import json
from django.conf import settings
from .models import Geojson
def add_geojson_data_from_json(json_file_path):
    media_root = settings.MEDIA_ROOT
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    for entry in data:
        state_name = entry.get("state")

        state_geojson_src = entry.get("state_geojson").strip()
        district_geojson_src = entry.get("district_geojson").strip()
        sub_district_geojson_src = entry.get("sub_district_geojson").strip()
        block_geojson_src = entry.get("block_geojson").strip()
        pincode_geojson_src = entry.get("pincode_geojson").strip()
        gram_panchayat_geojson_src = entry.get("gram_panchayat_geojson").strip()
        town_village_geojson_src = entry.get("town_village_geojson").strip()


        state_geojson_dest = f"1state_geojson/{os.path.basename(state_geojson_src)}"
        district_geojson_dest = f"2district_geojsons/{os.path.basename(district_geojson_src)}"
        sub_district_geojson_dest = f"3sub_district_geojson/{os.path.basename(sub_district_geojson_src)}"
        block_geojson_dest = f"4block_geojson/{os.path.basename(block_geojson_src)}"
        pincode_geojson_dest = f"5pincode_geojson/{os.path.basename(pincode_geojson_src)}"
        gram_panchayat_geojson_dest = f"6gram_panchayat_geojson/{os.path.basename(gram_panchayat_geojson_src)}"
        town_village_geojson_dest = f"7town_village_geojson/{os.path.basename(town_village_geojson_src)}"


        os.makedirs(os.path.join(media_root, '1state_geojson'), exist_ok=True)
        os.makedirs(os.path.join(media_root, '2district_geojsons'), exist_ok=True)
        os.makedirs(os.path.join(media_root, '3sub_district_geojson'), exist_ok=True)
        os.makedirs(os.path.join(media_root, '4block_geojson'), exist_ok=True)
        os.makedirs(os.path.join(media_root, '5pincode_geojson'), exist_ok=True)
        os.makedirs(os.path.join(media_root, '6gram_panchayat_geojson'), exist_ok=True)
        os.makedirs(os.path.join(media_root, '7town_village_geojson'), exist_ok=True)
        

        if os.path.exists(state_geojson_src):
            shutil.copy(state_geojson_src, os.path.join(media_root, state_geojson_dest))
        if os.path.exists(district_geojson_src):
            shutil.copy(district_geojson_src, os.path.join(media_root, district_geojson_dest))
        if os.path.exists(sub_district_geojson_src):
            shutil.copy(sub_district_geojson_src, os.path.join(media_root, sub_district_geojson_dest))
        if os.path.exists(block_geojson_src):
            shutil.copy(block_geojson_src,os.path.join(media_root,block_geojson_dest))
        if os.path.exists(pincode_geojson_src):
            shutil.copy(pincode_geojson_src,os.path.join(media_root,pincode_geojson_dest))
        if os.path.exists(gram_panchayat_geojson_src):
            shutil.copy(gram_panchayat_geojson_src,os.path.join(media_root,gram_panchayat_geojson_dest))
        if os.path.exists(town_village_geojson_src):
            shutil.copy(town_village_geojson_src,os.path.join(media_root,town_village_geojson_dest))

        Geojson.objects.create(
            state_name=state_name,

            state_geojson=state_geojson_dest,  # Use relative paths
            district_geojson=district_geojson_dest,
            sub_district_geojson=sub_district_geojson_dest,
            block_geojson=block_geojson_dest,
            pincode_geojson=pincode_geojson_dest,
            gram_panchayat_geojson=gram_panchayat_geojson_dest,
            town_village_geojson=town_village_geojson_dest,
        )
    print("GeoJSON data has been successfully added to the database.")

# add_geojson_data_from_json('/home/abhishek/Downloads/mapsofbharat/heatmap😁/json_db.json')

