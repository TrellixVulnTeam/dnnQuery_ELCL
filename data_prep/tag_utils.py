# Generating a tag utils
# By Hongyu Xiong, 04/02/2017

import math
import os
import random
import sys
import time
import re

import editdistance as ed
import numpy as np
import scratch

class Config(object):
    word_dim = 100
    vocabulary_path = '../data/vocab10000.from'
    glove_path = '../../glove.6B/glove.6B.100d.txt'
    max_vocabulary_size = 50000

    embedding_matrix, vocab, word_vector = scratch.generateEmbedMatrix(vocabulary_path, max_vocabulary_size, glove_path)
    # all keys for word_vector are in lowercase

    field2word = {
			'sum': {'value_type': 'string', 
                       'value_range': [], 
                       'query_word': ['sum','summation','total', 'combined']},
			'diff': {'value_type': 'string', 
                       'value_range': [], 
                       'query_word': ['difference']},
			'less': {'value_type': 'string', 
                       'value_range': [], 
                       'query_word': ['less']},
			'greater': {'value_type': 'string', 
                       'value_range': [], 
                       'query_word': ['more','larger']},
      'mean': {'value_type': 'string', 
                       'value_range': [], 
                       'query_word': []},
			'argmax': {'value_type': 'string', 
                       'value_range': ['maximum','max' ,'last'],#
                       'query_word': ['most','greatest','greatest','mean', 'average']}, # 'previous','before'
			'argmin': {'value_type': 'string', 
                       'value_range': [], #, 'next','after'
                       'query_word': ['least','minimum','first']},
			'Masters': {'value_type':'int',
						'query_word': ['masters']},
			'Country':{'value_type': 'string', 
                     'value_range': ['Brazil', 'Canada', 'Qatar', 'Italy', 'Peru', 'Kuwait', 'New_Zealand', 'Luxembourg', 'France',
                        'HK', 'Slovakia', 'Ireland', 'Nigeria', 'Norway', 'Argentina', 'South_Korea', 'Israel',
                        'Australia', 'Iran', 'Indonesia', 'West_Germany', 'Iceland', 'Slovenia', 'China', 'Chile',
                        'Belgium', 'Germany', 'Iraq', 'Philippines', 'Poland', 'Spain', 'Ukraine', 'Hungary',
                        'Netherlands', 'Denmark', 'Turkey', 'Finland', 'Sweden', 'Vietnam', 'Thailand', 'Switzerland',
                        'Russia', 'Pakistan', 'Romania', 'Portugal', 'Mexico', 'Egypt', 'Soviet_Union', 'Singapore',
                        'India', 'Liechtenstein', 'US', 'Czech', 'Austria', 'Yugoslavia', 'Saudi_Arabia', 'UK',
                        'Greece', 'Japan', 'Taiwan','Scotland','Mongolia','England','Kazakhstan','Nepal','Wales','Moldova',
                        'Belarus','Latvia','Armenia','United_States','Czech_Republic','Jamaica','Great_Britain','Uzbekistan',
                        'Malaysia','Uganda','Estonia','Croatia','Cuba','Morocco'], 
                     'query_word': ['country','nation','countries','nations','team','who']},
      'U.S._Open': {'value_type':'int',
						'query_word': ['u.s._open']},
			'The_Open': {'value_type':'int',
						'query_word': ['the_open']},
			'PGA': {'value_type':'int',
						'query_word': ['pga']},
			'Team':{'value_type': 'string', 
                     'value_range': ['Greystones','Ballymore_Eustace','Maynooth','Ballyroan_Abbey','Fingal_Ravens','Confey',
                        'Crettyard','Wolfe_Tones','Dundalk_Gael',
                        'Brazil', 'Canada', 'Qatar', 'Italy', 'Peru', 'Kuwait', 'New_Zealand', 'Luxembourg', 'France',
                        'HK', 'Slovakia', 'Ireland', 'Nigeria', 'Norway', 'Argentina', 'South_Korea', 'Israel',
                        'Australia', 'Iran', 'Indonesia', 'West_Germany', 'Iceland', 'Slovenia', 'China', 'Chile',
                        'Belgium', 'Germany', 'Iraq', 'Philippines', 'Poland', 'Spain', 'Ukraine', 'Hungary',
                        'Netherlands', 'Denmark', 'Turkey', 'Finland', 'Sweden', 'Vietnam', 'Thailand', 'Switzerland',
                        'Russia', 'Pakistan', 'Romania', 'Portugal', 'Mexico', 'Egypt', 'Soviet_Union', 'Singapore',
                        'India', 'Liechtenstein', 'US', 'Czech', 'Austria', 'Yugoslavia', 'Saudi_Arabia', 'UK',
                        'Greece', 'Japan', 'Taiwan','Scotland','Mongolia','England','Kazakhstan','Nepal','Wales','Moldova',
                        'Belarus','Latvia','Armenia','United_States','Czech_Republic','Jamaica','Great_Britain','Uzbekistan',
                        'Malaysia','Uganda','Estonia','Croatia','Cuba','Morocco'], 
                     'query_word': ['team','nation','country','who']},
      'County':{'value_type': 'string', 
                     'value_range': ['Wicklow','Kildare','Laois','Dublin','Meath','Louth'], 
                     'query_word': ['county','counties']},
      'Years': {'value_type':'date',
						'query_word': ['years','year','when']},
			'Years_won': {'value_type':'date',
            'query_word': ['years','year','when']},
      'Wins': {'value_type':'int',
						'query_word': []},
			'Areas': {'value_type':'int',
						'query_word': ['area','areas']},
			'Prices': {'value_type':'int',
						'query_word': ['prices', 'price']},
      'Swara': {'value_type': 'string', 
                     'value_range': ['Shadja','Shuddha_Rishabha','Chatushruti_Rishabha','Shuddha_Gandhara','Shatshruti_Rishabha',
                     'Sadharana_Gandhara','Antara_Gandhara','Shuddha_Madhyama','Prati_Madhyama','Panchama','Shuddha_Dhaivata',
                     'Chatushruti_Dhaivata','Shuddha_Nishada','Shatshruti_Dhaivata','Kaisiki_Nishada','Kakali_Nishada'], 
                     'query_word': ['swara']},
      'Short_name': {'value_type': 'string', 
                     'value_range': ['Pa','Sa','Ga','Gu','Gi','Ra','Ri','Ru','Ma','Mi','Dha','Dhi','Dhu','Na','Ni','Nu'], 
                     'query_word': ['short_name']},
      'Notation': {'value_type': 'string', 
                     'value_range': ['S','R1','R2','R3','G1','G2','G3','M1','M2','M3','D1','D2','D3','N1','N2','N3'], 
                     'query_word': ['notation']},
      'Mnemonic': {'value_type': 'string', 
                     'value_range': ['pa','sa','ga','gi','gu','ra','ri','ru','gi','gu','ma','mi','dha','dhi','dhu','na','ni','nu'], 
                     'query_word': ['mnemonic']},
			'Player': {'value_type': 'string', 
                     'value_range': ['Herbie_Hewett','Lionel_Palairet','Bill_Roe','George_Nichols','John_Challen','Ted_Tyler',
                     'Crescens_Robinson','Albert_Clapp','John_Felmley','Gordon_Otto','Ernest_McKay','George_Halas','Ralf_Woods'], 
                     'query_word': ['player','who']},
			'Matches': {'value_type':'int',
						'query_word': ['matches','match']},
			'Innings': {'value_type':'int',
						'query_word': ['innings']},
			'Runs': {'value_type':'int',
						'query_word': ['runs','run']},
			'Average': {'value_type':'int',
						'query_word': ['average']},
			'100s': {'value_type':'int',
						'query_word': ['100s']},
			'50s': {'value_type':'int',
						'query_word': ['50s']},
			'Games_Played': {'value_type':'int',
						'query_word': ['games']},
			'Field_Goals': {'value_type':'int',
						'query_word': ['field', 'goals']},
			'Free_Throws': {'value_type':'int',
						'query_word': ['free', 'throws']},
			'Points': {'value_type':'int',
						'query_word': ['points']},
			'Menteri_Besar': {'value_type': 'string', 
                     'value_range': ['Jaafar_Mohamed','Mohamed_Mahbob','Abdullah_Jaafar','Mustapha_Jaafar','Abdul_Hamid_Yusof',
                                      'Ungku_Abdul_Aziz_Abdul_Majid','Onn_Jaafar','Syed_Abdul_Kadir_Mohamed','Wan_Idris_Ibrahim'], 
                     'query_word': ['menteri_besar']},
			'Party':{'value_type': 'string', 
                     'value_range': ['Conservatives','Green','Socialist_Alternative','Independent','Labour','Respect','No_party',
                     'Liberal_Democrats'], 
                     'query_word': ['party']},
			'Took_office':{'value_type': 'date', 
                     'value_range': ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August','September', 'December', 'November', 'October'], 
                     'query_word': ['take_office']},
      'Left_office':{'value_type': 'date', 
                     'value_range': ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August','September', 'December', 'November', 'October'], 
                     'query_word': ['leave_office']},
			'Nation':{'value_type': 'string', 
                     'value_range': ['Brazil', 'Canada', 'Qatar', 'Italy', 'Peru', 'Kuwait', 'New_Zealand', 'Luxembourg', 'France',
                        'HK', 'Slovakia', 'Ireland', 'Nigeria', 'Norway', 'Argentina', 'South_Korea', 'Israel',
                        'Australia', 'Iran', 'Indonesia', 'West_Germany', 'Iceland', 'Slovenia', 'China', 'Chile',
                        'Belgium', 'Germany', 'Iraq', 'Philippines', 'Poland', 'Spain', 'Ukraine', 'Hungary',
                        'Netherlands', 'Denmark', 'Turkey', 'Finland', 'Sweden', 'Vietnam', 'Thailand', 'Switzerland',
                        'Russia', 'Pakistan', 'Romania', 'Portugal', 'Mexico', 'Egypt', 'Soviet_Union', 'Singapore',
                        'India', 'Liechtenstein', 'US', 'Czech', 'Austria', 'Yugoslavia', 'Saudi_Arabia', 'UK',
                        'Greece', 'Japan', 'Taiwan','Scotland','Mongolia','England','Kazakhstan','Nepal','Wales','Moldova',
                        'Belarus','Latvia','Armenia','United_States','Czech_Republic','Jamaica','Great_Britain','Uzbekistan',
                        'Malaysia','Uganda','Estonia','Croatia','Cuba','Morocco'], 
                     'query_word': ['country','nation','countries','nations','team','who']},
			'Rank': {'value_type':'ordinal',
            #'value_range': ['first', 'second', 'third', '1st', '2nd', '3rd','last'],
						'query_word': ['rank', 'ranked']},
			'Gold': {'value_type':'int',
						'query_word': ['gold']},
			'Silver': {'value_type':'int',
						'query_word': ['silver']},
			'Bronze': {'value_type':'int',
						'query_word': ['bronze']},
			'Total': {'value_type':'int',
						'query_word': ['total']},
			'Name': {'value_type':'string',
						'value_range': ['Ned_Barkas','Harry_Brough','George_Brown','Jack_Byers','Ernie_Islip','Billy_Johnston','Robert_Jones',
            'Frank_Mann','Len_Marlow','Colin_McKay','Sandy_Mutch','Stan_Pearson','George_Richardson','Charlie_Slade',
            'Billy_E._Smith','Billy_H._Smith','Clem_Stephenson','Jack_Swann','Sam_Wadsworth','Billy_Watson','Tom_Wilson',
            'James_Wood','Tommy_Mooney','Duncan_Welbourne','Luther_Blissett','John_McClelland','David_James','Ross_Jenkins',
            'Nigel_Gibbs','Les_Taylor','Tony_Coton','Ian_Bolton','Robert_Page'],
						'query_word': ['name','who']},
			'Position': {'value_type':'string',
						'value_range':['Goalkeeper','Defender','Midfielder','Forward'],
						'query_word': ['position']},
			'Year_inducted': {'value_type':'date',
						'query_word': ['year','years','when']},
			'Apps': {'value_type':'int',
						'query_word': ['appearance','appearances']},
			'Discipline': {'value_type':'string',
            'value_range': ['Hurdles', 'Cycling', 'Swimming', 'Curling', 'Archery', 'Hammer'],
            'query_word': []},
      'Amanda':{'value_type':'int',
            'query_word': ['amanda']},
      'Bernie':{'value_type':'int',
            'query_word': ['bernie']},
      'Javine_H':{'value_type':'int',
            'query_word': ['javine_h']},
      'Julia':{'value_type':'int',
            'query_word': ['julia']},
      'Michelle':{'value_type':'int',
            'query_word': ['michelle']},
      'Goals': {'value_type':'int',
						'query_word': ['goal','goals']},
			'Total_Apps': {'value_type':'int',
						'query_word': ['appearance','appearances']},
			'Total_Goals': {'value_type':'int',
						'query_word': ['goal','goals']},
			'League_Apps': {'value_type':'int',
						'query_word': ['appearance','appearances']},
			'League_Goals': {'value_type':'int',
						'query_word': ['goal','goals']},
			'FA_Cup_Apps': {'value_type':'int',
						'query_word': ['appearance','appearances']},
			'FA_Cup_Goals': {'value_type':'int',
						'query_word': ['goal','goals']},
			'State': {'value_type':'string',
						'value_range':['California','Texas','Florida','Louisiana','Bihar','Assam','Himachal_Pradesh','Manipur',
            'Chhattisgarh','Tamil_Nadu','Jammu_and_Kashmir','Karnataka','Mizoram','Kerala','Gujarat','Rajasthan','Uttarakhand',
            'Maharashtra','Madhya_Pradesh','West_Bengal','Meghalaya','Tripura','Delhi','Goa','Punjab','Puducherry',
            'Uttar_Pradesh','Odisha','Andhra_Pradesh','Haryana'],
						'query_word': ['state','county']},
			'No._of_elected': {'value_type':'int',
						'query_word': ['elected']},
			'No._of_candidates': {'value_type':'int',
						'query_word': ['candidate', 'candidates']},
			'Total_no._of_seats_in_Assembly': {'value_type':'int',
						'query_word': ['seat', 'seats']},
			'Year_of_Election': {'value_type':'date',
						'query_word': ['year','years','when']},
			'Year': {'value_type':'date',
						'query_word': ['year','years','when']},
			'1st_Venue': {'value_type': 'string', 
                       'value_range': ['Sheffield','Tijuana','Doha','Qingdao','Moscow','Dubai','Beijing','Sydney'], 
                       'query_word': ['city','1st_venue']}, 
      '2nd_Venue': {'value_type': 'string', 
                       'value_range': ['Mexico_City','Changzhou','Sheffield','Veracruz','Beijing','Dubai',
                       'Havana','Cambridge','Boston','Nassau','Detroit','Hangzhou','Indianapolis','Shanghai',
                       'Washington'], 
                       'query_word': ['city', '2nd_venue']}, 
      '3rd_Venue': {'value_type': 'string', 
                       'value_range': ['Nanjing','Sheffield','Moscow','Veracruz','Edinburgh','London','Chicago',
                       'Hangzhou','Austin','Minneapolis'], 
                       'query_word': ['city', '3rd_venue']}, 
      '4th_Venue': {'value_type': 'string', 
                       'value_range': ['NA','Tijuana','Guanajuato','Moscow','Sydney','Los_Angeles','Tokyo'], 
                       'query_word': ['city', '4th_venue']}, 
      '5th_Venue': {'value_type': 'string', 
                       'value_range': ['NA','Guadalajara','Windsor'], 
                       'query_word': ['city', '5th_venue']}, 
      '6th_Venue': {'value_type': 'string', 
                       'value_range': ['NA','Guadalajara','Monterrey'], 
                       'query_word': ['city', '6th_venue']}, 
	 #       'host_city':{'value_type': 'string', 
   #                     'value_range': ['Amsterdam', 'Antwerp', 'Athens', 'Atlanta', 'Bangkok', 'Barcelona', 'Beijing', 'Berlin',
   #                        'Budapest', 'Buenos_Aires', 'Cairo', 'Cape_Town', 'Chamonix', 'Chicago', 'Cortina_Ampezzo',
   #                        'Dallas', 'Delhi', 'Dubai', 'Dublin', 'Florence', 'Grenoble', 'Helsinki', 'Hong_Kong',
   #                        'Innsbruck', 'Istanbul', 'Jerusalem', 'Lake_Placid', 'Las_Vegas', 'London', 'Los_Angeles',
   #                        'Madrid', 'Melbourne', 'Mexico_City', 'Milan', 'Montreal', 'Moscow', 'Mumbai', 'Munich',
   #                        'New_York', 'Oslo', 'Paris', 'Philadelphia', 'Prague', 'Rio_de_Janeiro', 'Rome', 'San_Diego',
   #                        'Sapporo', 'Sarajevo', 'Seattle', 'Seoul', 'Macau', 'Squaw_Valley', 'St._Moritz',
   #                        'Stockholm', 'Sydney', 'Tokyo', 'Toronto', 'Venice', 'Vienna', 'Warsaw'], 
   #                     'query_word': ['city', 'cities']}, 
   #      	'#_participants':{'value_type': 'int', 
   #                          'query_word': ['participate', 'participates', 'participated', 'participant', 'participants']},
   #      	'#_audience':{'value_type': 'int', 
   #                      'query_word': ['audience']},
   #      	'#_medals':{'value_type': 'int', 
   #                    'query_word': ['medal', 'medals']},
   #      	'country_size':{'value_type': 'int', 
   #                        'query_word': ['large', 'larger', 'largest']}, 
   #      	'country_gdp':{'value_type': 'int', 
   #                       'query_word': ['gdp', 'wealth', 'wealthy', 'wealthier']}, 
   #      	'country_population':{'value_type': 'int', 
   #                              'query_word': ['population', 'people']}, 
   #      	'#_duration':{'value_type': 'int', 
   #                      'query_word': ['long', 'longer', 'longest', 'duration', 'day', 'days']},
   #      	'year':{'value_type': 'int', 
   #                'query_word': ['year', 'years','when']}, 
   #      	'country':{'value_type': 'string', 
   #                   'value_range': ['Brazil', 'Canada', 'Qatar', 'Italy', 'Peru', 'Kuwait', 'New_Zealand', 'Luxembourg', 'France',
   #                      'HK', 'Slovakia', 'Ireland', 'Nigeria', 'Norway', 'Argentina', 'South_Korea', 'Israel',
   #                      'Australia', 'Iran', 'Indonesia', 'West_Germany', 'Iceland', 'Slovenia', 'China', 'Chile',
   #                      'Belgium', 'Germany', 'Iraq', 'Philippines', 'Poland', 'Spain', 'Ukraine', 'Hungary',
   #                      'Netherlands', 'Denmark', 'Turkey', 'Finland', 'Sweden', 'Vietnam', 'Thailand', 'Switzerland',
   #                      'Russia', 'Pakistan', 'Romania', 'Portugal', 'Mexico', 'Egypt', 'Soviet_Union', 'Singapore',
   #                      'India', 'Liechtenstein', 'US', 'Czech', 'Austria', 'Yugoslavia', 'Saudi_Arabia', 'UK',
   #                      'Greece', 'Japan', 'Taiwan','Scotland','Mongolia','England','Kazakhstan','Nepal'], 
   #                   'query_word': ['country','nation','countries','nations']}
      }

