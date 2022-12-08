#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:52:43 2020

@author: samkoenig
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import pandas as pd

#Read Individual CSV Files 
Student_List = pd.read_csv(r"C:\Users\Sam Koenig\Desktop\MyOptions Analysis\Student List.csv",header=0,encoding = 'unicode_escape')
Colleges = pd.read_csv(r"C:\Users\Sam Koenig\Desktop\MyOptions Analysis\Master College List.csv",header=0,encoding = 'unicode_escape')

#Join College Profiles
Final_Student_List = pd.merge(Student_List, Colleges, left_on='College/University: OneGoal ID', right_on='OneGoal ID',how='left')

#Replace Spaces in the column headers of data file
Final_Student_List.columns = Final_Student_List.columns.str.replace(' ', '_')

#Replaces null values with 0 in recommended institution field
Final_Student_List.Recommended_Institution = Final_Student_List[['Recommended_Institution']].fillna(0)


#Defining In State Function
def In_State (row):
   if row['State'] == 'IL' and row['Region_x'] == "Chicago" :
      return 1
   elif row['State'] == 'TX' and row['Region_x'] == "Houston":
      return 1
   elif row['State'] == 'NY' and row['Region_x'] == "New York":
       return 1 
   elif row['State'] == 'CA' and row['Region_x'] == "Bay Area":
       return 1 
   elif row['State'] == 'GA' and row['Region_x'] == "Metro Atlanta":
       return 1 
   elif row['State'] == 'MA' and row['Region_x'] == "Massachusetts":
       return 1 
   return 0 


#Adding In State Column to Final Student List dataframe
Final_Student_List['In_State'] = Final_Student_List.apply(In_State, axis=1)


#Defining Match function
def Match_Count (row):
    if row['Match_Rating'] == 'Match':
        return 1
    return 0

#Adding Match to Final Student List dataframe
Final_Student_List['Match_Count'] = Final_Student_List.apply(Match_Count, axis=1)

#Defining Net Price Count over 15000 function
def Net_Price_Count (row):
    if row['Net_Price:_0-30'] > 15000:
        return 1
    return 0

#Adding net price to dataframe
Final_Student_List['Net_Price_Count'] = Final_Student_List.apply(Net_Price_Count, axis=1)

#Adding URM over 57.6
def URM_Graduation_57 (row):
    if row['URM_Graduation_Rate'] > 57.6:
        return 1
    return 0

#Adding URM Graduation Rate 57 Count to dataframe
Final_Student_List['URM_Graduation_57'] = Final_Student_List.apply(URM_Graduation_57, axis=1)


#Convert 6 Year Graduation Rate to Float
Final_Student_List['URM_Graduation_Rate'] = Final_Student_List['URM_Graduation_Rate'].astype('float64')

#Convert Net Price of School to a Float
Final_Student_List['Net_Price:_0-30'] = Final_Student_List['Net_Price:_0-30'].astype('float64')


#Grouping the final output by each student
Final_Student_List = Final_Student_List.groupby(['Case_Safe_ID','Year']).agg({'Case_Safe_ID': 'count', 'In_State': 'sum', 'URM_Graduation_Rate': 'mean','Match_Count':'sum'})


Final_Student_List.columns = ['Number_of_Schools','Number_In_State','URM_Graduation_Rate','Match_Count']

#Calculate percent of schools that are in state
def Percent_In_State (row):
    return (row['Number_In_State']/ row['Number_of_Schools'])*100

#Add transformed count schools to dataframe
Final_Student_List['Percent_In_State'] = Final_Student_List.apply(Percent_In_State, axis=1)


def Match_Percent (row):
    return (row['Match_Count']/ row['Number_of_Schools'])*100

#Add Match_Percent to dataframe
Final_Student_List['Match_Percent'] = Final_Student_List.apply(Match_Percent, axis=1)

#Tranform the data based on the number of schools on a list
def Count_Schools (row):
    if row['Number_of_Schools'] >= 12:
        return 100
    elif row['Number_of_Schools'] >= 7:
        return 75
    elif row['Number_of_Schools'] >= 5:
        return 50
    elif row['Number_of_Schools'] >= 4:
        return 25
    elif row['Number_of_Schools'] < 4:
        return 0
    
#Add transformed count schools to dataframe
Final_Student_List['Count_Schools_Transformed'] = Final_Student_List.apply(Count_Schools, axis=1)

#Convert percentage of schools in state on a scale from 1-100
def In_State_Cutscores (row):
    if row['Percent_In_State'] >=60:
        return 100
    elif row['Percent_In_State'] >= 50:
        return 75
    elif row['Percent_In_State'] >= 30:
        return 50
    elif row['Percent_In_State'] >= 10:
        return 25
    elif row['Percent_In_State'] < 10:
        return 0
    

#Add transformed percentage of schools on list in state to dataframe
Final_Student_List['In_State_Transformed'] = Final_Student_List.apply(In_State_Cutscores, axis=1)
    
#Convert Graduation Rate Minority in state on a scale from 1-100
def Six_Year_Grad_Rate_Minority (row):
    if row['URM_Graduation_Rate'] >=55:
        return 100
    elif row['URM_Graduation_Rate'] >= 45:
        return 75
    elif row['URM_Graduation_Rate'] >= 35:
        return 50
    elif row['URM_Graduation_Rate'] >= 25:
        return 25
    elif row['URM_Graduation_Rate'] < 25:
        return 0
    
#Add transformed count schools to dataframe
Final_Student_List['6_Year_Graduation_Rate_URM'] = Final_Student_List.apply(Six_Year_Grad_Rate_Minority, axis=1)



#Convert percentage of schools recommneded by OneGoal on a scale from 1-4
def Match_Transformed (row):
    if row['Match_Percent'] >= 70:
        return 50
    elif row['Match_Percent'] >= 50:
        return 100
    elif row['Match_Percent'] >= 40:
        return 75
    elif row['Match_Percent'] >= 30:
        return 50
    elif row['Match_Percent'] >= 20:
        return 25
    elif row['Match_Percent'] < 20:
        return 0
    

#Add transformed percentage of schools that are Match to dataframe
Final_Student_List['Match_Transformed'] = Final_Student_List.apply(Match_Transformed, axis=1)


#Convert metrics to float before final list quality scoree calculation
Final_Student_List['Count_Schools_Transformed'] = Final_Student_List['Count_Schools_Transformed'].astype('float64')
Final_Student_List['Match_Transformed']= Final_Student_List['Match_Transformed'].astype('float64')
Final_Student_List['In_State_Transformed'] = Final_Student_List['In_State_Transformed'].astype('float64')
Final_Student_List['6_Year_Graduation_Rate_URM'] = Final_Student_List['6_Year_Graduation_Rate_URM'].astype('float64')


#Calculate final list_quality_score
def list_quality_score (row):
    return (row['Count_Schools_Transformed'] + row['Match_Transformed'] + row['In_State_Transformed'] + row['6_Year_Graduation_Rate_URM'])/4

    
#Add final list_quality_score to final export
Final_Student_List['List_Quality_Score'] = Final_Student_List.apply(list_quality_score, axis=1)

#Output to csv
Final_Student_List.to_csv('List Quality Score Historical.csv')

