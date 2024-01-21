
# List Quality Score Transformation
This is simple python transformation to transform two csv files: 

 - Master College List.csv - A file containing data on 2 and 4 year colleges in the United States. This data is directly taken from the NCES Integrated Postsecondary Education System [here](https://nces.ed.gov/ipeds/use-the-data)
 - Student List.csv - A file of a list of a students and their current college lists. This is a file that is a pretty standard export from our Salesforce college_application_list report, although the data provided here is fake. 

The purpose of this code is to analyze students lists, and apply a standardized list quality "score" to assess quality based on important factors that correlate to a students ability to persist after leaving high school. 

**The variables of interest here are:** 
 **1. Number of Schools** - How many schools are on the students lists?
 **2. In State** - What percentage of the schools are In the students state? 
 **3. Match**  -What percentage of the schools are a match school?
 **4. URM Graduation Rate** - What is the average 6 year Underrepresented Minority Graduation Rate?

After, this will create a csv of aggregations on the four metrics above as well as the new measure for a school leader can use to prioritize intervention with the student. 

**Requirements**:
- Ensure that your own directory information is inputted in row 22/23 to read the csv of the Master College List file and the Student List csv file*
