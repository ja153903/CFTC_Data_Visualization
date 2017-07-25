from django.shortcuts import render
from django.views import View
import pandas as pd
from collections import Counter
import datetime

# Create your views here.

class AreaChartView(View):

	def get(self, request):

		agriculture_mm, energy_mm, metals_mm, total_mm = self.managed_money_positions()
		agriculture_pm, energy_pm, metals_pm, total_pm = self.prod_merc_positions()
		agriculture_s, energy_s, metals_s, total_s = self.swap_positions()
		agriculture_or, energy_or, metals_or, total_or = self.other_rept_positions()
		agriculture_tr, energy_tr, metals_tr, total_tr = self.tot_rept_positions()

		return render(request, 'AreaChart/index.html', 
		{
		'agriculture_mm': agriculture_mm, 
		'energy_mm': energy_mm,
		'metals_mm': metals_mm, 
		'total_mm': total_mm,
		'agriculture_pm': agriculture_pm,
		'energy_pm': energy_pm,
		'metals_pm': metals_pm,
		'total_pm': total_pm,
		'agriculture_s': agriculture_s,
		'energy_s': energy_s,
		'metals_s': metals_s,
		'total_s': total_s,
		'agriculture_or': agriculture_or,
		'energy_or': energy_or,
		'metals_or': metals_or,
		'total_or': total_or,
		'agriculture_tr': agriculture_tr,
		'energy_tr': energy_tr,
		'metals_tr': metals_tr,
		'total_tr': total_tr,
		})

	def get_data(self):
		cftc_master_data = pd.read_excel('AreaChart/data/f_year.xls', sheetname='XLS')

		columns = ['Market_and_Exchange_Names', 'As_of_Date_In_Form_YYMMDD', 'Report_Date_as_MM_DD_YYYY',
		           'CFTC_Contract_Market_Code',	'CFTC_Market_Code',	'CFTC_Region_Code',	'CFTC_Commodity_Code',
		           'Open_Interest_All',	'Prod_Merc_Positions_Long_ALL',	'Prod_Merc_Positions_Short_ALL',
		           'Swap_Positions_Long_All', 'Swap__Positions_Short_All', 'Swap__Positions_Spread_All',
		           'M_Money_Positions_Long_ALL', 'M_Money_Positions_Short_ALL',
		           'M_Money_Positions_Spread_ALL', 'Market_Type',
		           'Other_Rept_Positions_Long_ALL',	'Other_Rept_Positions_Short_ALL', 'Other_Rept_Positions_Spread_ALL',
		           'Tot_Rept_Positions_Long_All', 'Tot_Rept_Positions_Short_All','NonRept_Positions_Long_All',
		           'NonRept_Positions_Short_All', 'Traders_Tot_All', 'Traders_Prod_Merc_Long_All', 'Traders_Prod_Merc_Short_All',
		           'Traders_Swap_Long_All',	'Traders_Swap_Short_All', 'Traders_Swap_Spread_All', 'Traders_M_Money_Long_All',
		           'Traders_M_Money_Short_All',	'Traders_M_Money_Spread_All', 'Traders_Other_Rept_Long_All',
		           'Traders_Other_Rept_Short_All', 'Traders_Other_Rept_Spread_All',	'Traders_Tot_Rept_Long_All',
		           'Traders_Tot_Rept_Short_All', 'Conc_Gross_LE_4_TDR_Long_All', 'Conc_Gross_LE_4_TDR_Short_All',
		           'Conc_Gross_LE_8_TDR_Long_All',	'Conc_Gross_LE_8_TDR_Short_All', 'Conc_Net_LE_4_TDR_Long_All',
		           'Conc_Net_LE_4_TDR_Short_All', 'Conc_Net_LE_8_TDR_Long_All',	'Conc_Net_LE_8_TDR_Short_All',
		           'Conc_Gross_LE_4_TDR_Long_Old', 'Conc_Gross_LE_4_TDR_Short_Old',	'Conc_Gross_LE_8_TDR_Long_Old',
		           'Conc_Gross_LE_8_TDR_Short_Old',	'Conc_Net_LE_4_TDR_Long_Old', 'Conc_Net_LE_4_TDR_Short_Old',
		           'Conc_Net_LE_8_TDR_Long_Old', 'Conc_Net_LE_8_TDR_Short_Old',	'Conc_Gross_LE_4_TDR_Long_Other',
		           'Conc_Gross_LE_4_TDR_Short_Other', 'Conc_Gross_LE_8_TDR_Long_Other',	'Conc_Gross_LE_8_TDR_Short_Other',
		           'Conc_Net_LE_4_TDR_Long_Other', 'Conc_Net_LE_4_TDR_Short_Other',	'Conc_Net_LE_8_TDR_Long_Other',
		           'Conc_Net_LE_8_TDR_Short_Other',	'Contract_Units', 'CFTC_SubGroup_Code',	'FutOnly_or_Combined'
		]

		cftc_needed_data = cftc_master_data[columns].copy()

		return cftc_needed_data


	def managed_money_positions(self):

		cftc_needed_data = self.get_data()

		cftc_managed_money = cftc_needed_data[[
		    'Market_and_Exchange_Names',
		    'Report_Date_as_MM_DD_YYYY',
		    'Market_Type',
		    'M_Money_Positions_Long_ALL',
		    'M_Money_Positions_Short_ALL',
		    'Traders_M_Money_Long_All',
		    'Traders_M_Money_Short_All']].copy()
		cftc_managed_money['M_Money_Positions_Combined_ALL'] = cftc_managed_money['M_Money_Positions_Long_ALL'] - cftc_managed_money['M_Money_Positions_Short_ALL']
		cftc_managed_money['Traders_M_Money_Combined_ALL'] = cftc_needed_data['Traders_M_Money_Long_All'] + cftc_needed_data['Traders_M_Money_Short_All']
		agriculture_df = cftc_managed_money[cftc_managed_money['Market_Type'] == 'Agriculture'].sort_values('Report_Date_as_MM_DD_YYYY')
		energy_df = cftc_managed_money[cftc_managed_money['Market_Type'] == 'Energy'].sort_values('Report_Date_as_MM_DD_YYYY')
		metals_df = cftc_managed_money[cftc_managed_money['Market_Type'] == 'Metals'].sort_values('Report_Date_as_MM_DD_YYYY')

		# create a dictionary of values that hold the sum of each date
		def create_sum_dict(df):
		    map = {}

		    for date in df['Report_Date_as_MM_DD_YYYY']:
		        if str(date.date()) not in map:
		            map[str(date.date())] = 0

		    for index, value in df.iterrows():
		        map[str(value['Report_Date_as_MM_DD_YYYY'].date())] += value['M_Money_Positions_Combined_ALL']

		    return map

		# Bucket the values into one value
		mm_agriculture_dict = create_sum_dict(agriculture_df)
		mm_energy_dict = create_sum_dict(energy_df)
		mm_metals_dict = create_sum_dict(metals_df)

		# Bucket all three into one value
		mm_total_dict = Counter()
		mm_total_dict.update(mm_agriculture_dict)
		mm_total_dict.update(mm_energy_dict)
		mm_total_dict.update(mm_metals_dict)

		mm_total_dict = dict(mm_total_dict)

		return mm_agriculture_dict, mm_energy_dict, mm_metals_dict, mm_total_dict

	def prod_merc_positions(self):

		cftc_needed_data = self.get_data()

		cftc_prod_merc = cftc_needed_data[[
		    'Market_and_Exchange_Names',
		    'Report_Date_as_MM_DD_YYYY',
		    'Market_Type',
		    'Prod_Merc_Positions_Long_ALL',
		    'Prod_Merc_Positions_Short_ALL',
		    'Traders_Prod_Merc_Long_All',
		    'Traders_Prod_Merc_Short_All']].copy()

		cftc_prod_merc['Prod_Merc_Positions_Combined_ALL'] = cftc_prod_merc['Prod_Merc_Positions_Long_ALL'] - cftc_prod_merc['Prod_Merc_Positions_Short_ALL']
		cftc_prod_merc['Traders_Prod_Merc_Combined_ALL'] = cftc_prod_merc['Traders_Prod_Merc_Long_All'] + cftc_prod_merc['Traders_Prod_Merc_Short_All']
		agriculture_df = cftc_prod_merc[cftc_prod_merc['Market_Type'] == 'Agriculture'].sort_values('Report_Date_as_MM_DD_YYYY')
		energy_df = cftc_prod_merc[cftc_prod_merc['Market_Type'] == 'Energy'].sort_values('Report_Date_as_MM_DD_YYYY')
		metals_df = cftc_prod_merc[cftc_prod_merc['Market_Type'] == 'Metals'].sort_values('Report_Date_as_MM_DD_YYYY')

		# create a dictionary of values that hold the sum of each date
		def create_sum_dict(df):
		    map = {}

		    for date in df['Report_Date_as_MM_DD_YYYY']:
		        if str(date.date()) not in map:
		            map[str(date.date())] = 0

		    for index, value in df.iterrows():
		        map[str(value['Report_Date_as_MM_DD_YYYY'].date())] += value['Prod_Merc_Positions_Combined_ALL']

		    return map

		# Bucket the values into one value
		pm_agriculture_dict = create_sum_dict(agriculture_df)
		pm_energy_dict = create_sum_dict(energy_df)
		pm_metals_dict = create_sum_dict(metals_df)

		# Bucket all three into one value
		pm_total_dict = Counter()
		pm_total_dict.update(pm_agriculture_dict)
		pm_total_dict.update(pm_energy_dict)
		pm_total_dict.update(pm_metals_dict)

		pm_total_dict = dict(pm_total_dict)

		return pm_agriculture_dict, pm_energy_dict, pm_metals_dict, pm_total_dict

	def swap_positions(self):

		cftc_needed_data = self.get_data()

		cftc_swap = cftc_needed_data[[
		    'Market_and_Exchange_Names',
		    'Report_Date_as_MM_DD_YYYY',
		    'Market_Type',
		    'Swap_Positions_Long_All',
		    'Swap__Positions_Short_All',
		    'Traders_Swap_Long_All',
		    'Traders_Swap_Short_All']].copy()

		cftc_swap['Swap_Positions_Combined_All'] = cftc_swap['Swap_Positions_Long_All'] - cftc_swap['Swap__Positions_Short_All']
		cftc_swap['Traders_Swap_Combined_All'] = cftc_swap['Traders_Swap_Long_All'] + cftc_swap['Traders_Swap_Short_All']
		agriculture_df = cftc_swap[cftc_swap['Market_Type'] == 'Agriculture'].sort_values('Report_Date_as_MM_DD_YYYY')
		energy_df = cftc_swap[cftc_swap['Market_Type'] == 'Energy'].sort_values('Report_Date_as_MM_DD_YYYY')
		metals_df = cftc_swap[cftc_swap['Market_Type'] == 'Metals'].sort_values('Report_Date_as_MM_DD_YYYY')

		# create a dictionary of values that hold the sum of each date
		def create_sum_dict(df):
		    map = {}

		    for date in df['Report_Date_as_MM_DD_YYYY']:
		        if str(date.date()) not in map:
		            map[str(date.date())] = 0

		    for index, value in df.iterrows():
		        map[str(value['Report_Date_as_MM_DD_YYYY'].date())] += value['Swap_Positions_Combined_All']

		    return map

		# Bucket the values into one value
		s_agriculture_dict = create_sum_dict(agriculture_df)
		s_energy_dict = create_sum_dict(energy_df)
		s_metals_dict = create_sum_dict(metals_df)

		# Bucket all three into one value
		s_total_dict = Counter()
		s_total_dict.update(s_agriculture_dict)
		s_total_dict.update(s_energy_dict)
		s_total_dict.update(s_metals_dict)

		s_total_dict = dict(s_total_dict)

		return s_agriculture_dict, s_energy_dict, s_metals_dict, s_total_dict

	def other_rept_positions(self):

		cftc_needed_data = self.get_data()

		cftc_other_rept = cftc_needed_data[[
		    'Market_and_Exchange_Names',
		    'Report_Date_as_MM_DD_YYYY',
		    'Market_Type',
		    'Other_Rept_Positions_Long_ALL',
		    'Other_Rept_Positions_Short_ALL',
		    'Traders_Other_Rept_Long_All',
		    'Traders_Other_Rept_Short_All']].copy()

		cftc_other_rept['Other_Rept_Positions_Combined_All'] = cftc_other_rept['Other_Rept_Positions_Long_ALL'] - cftc_other_rept['Other_Rept_Positions_Short_ALL']
		cftc_other_rept['Traders_Other_Rept_Combined_All'] = cftc_other_rept['Traders_Other_Rept_Long_All'] + cftc_other_rept['Traders_Other_Rept_Short_All']
		agriculture_df = cftc_other_rept[cftc_other_rept['Market_Type'] == 'Agriculture'].sort_values('Report_Date_as_MM_DD_YYYY')
		energy_df = cftc_other_rept[cftc_other_rept['Market_Type'] == 'Energy'].sort_values('Report_Date_as_MM_DD_YYYY')
		metals_df = cftc_other_rept[cftc_other_rept['Market_Type'] == 'Metals'].sort_values('Report_Date_as_MM_DD_YYYY')

		# create a dictionary of values that hold the sum of each date
		def create_sum_dict(df):
		    map = {}

		    for date in df['Report_Date_as_MM_DD_YYYY']:
		        if str(date.date()) not in map:
		            map[str(date.date())] = 0

		    for index, value in df.iterrows():
		        map[str(value['Report_Date_as_MM_DD_YYYY'].date())] += value['Other_Rept_Positions_Combined_All']

		    return map

		# Bucket the values into one value
		or_agriculture_dict = create_sum_dict(agriculture_df)
		or_energy_dict = create_sum_dict(energy_df)
		or_metals_dict = create_sum_dict(metals_df)

		# Bucket all three into one value
		or_total_dict = Counter()
		or_total_dict.update(or_agriculture_dict)
		or_total_dict.update(or_energy_dict)
		or_total_dict.update(or_metals_dict)

		or_total_dict = dict(or_total_dict)

		return or_agriculture_dict, or_energy_dict, or_metals_dict, or_total_dict

	def tot_rept_positions(self):

		cftc_needed_data = self.get_data()

		cftc_tot_rept = cftc_needed_data[[
		    'Market_and_Exchange_Names',
		    'Report_Date_as_MM_DD_YYYY',
		    'Market_Type',
		    'Tot_Rept_Positions_Long_All',
		    'Tot_Rept_Positions_Short_All',
		    'Traders_Tot_Rept_Long_All',
		    'Traders_Tot_Rept_Short_All']].copy()

		cftc_tot_rept['Tot_Rept_Positions_Combined_All'] = cftc_tot_rept['Tot_Rept_Positions_Long_All'] - cftc_tot_rept['Tot_Rept_Positions_Short_All']
		cftc_tot_rept['Traders_Tot_Rept_Combined_All'] = cftc_tot_rept['Traders_Tot_Rept_Long_All'] + cftc_tot_rept['Traders_Tot_Rept_Short_All']
		agriculture_df = cftc_tot_rept[cftc_tot_rept['Market_Type'] == 'Agriculture'].sort_values('Report_Date_as_MM_DD_YYYY')
		energy_df = cftc_tot_rept[cftc_tot_rept['Market_Type'] == 'Energy'].sort_values('Report_Date_as_MM_DD_YYYY')
		metals_df = cftc_tot_rept[cftc_tot_rept['Market_Type'] == 'Metals'].sort_values('Report_Date_as_MM_DD_YYYY')

		# create a dictionary of values that hold the sum of each date
		def create_sum_dict(df):
		    map = {}

		    for date in df['Report_Date_as_MM_DD_YYYY']:
		        if str(date.date()) not in map:
		            map[str(date.date())] = 0

		    for index, value in df.iterrows():
		        map[str(value['Report_Date_as_MM_DD_YYYY'].date())] += value['Tot_Rept_Positions_Combined_All']

		    return map

		# Bucket the values into one value
		tr_agriculture_dict = create_sum_dict(agriculture_df)
		tr_energy_dict = create_sum_dict(energy_df)
		tr_metals_dict = create_sum_dict(metals_df)

		# Bucket all three into one value
		tr_total_dict = Counter()
		tr_total_dict.update(tr_agriculture_dict)
		tr_total_dict.update(tr_energy_dict)
		tr_total_dict.update(tr_metals_dict)

		tr_total_dict = dict(tr_total_dict)

		return tr_agriculture_dict, tr_energy_dict, tr_metals_dict, tr_total_dict