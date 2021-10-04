import time , math
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#define google spread sheet service and credentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
#Authorazing this app
gc = gspread.authorize(credentials)
#Open sheet by key
wks = gc.open_by_key('1S72arIoo7MArC5XYe20BEynBD2Z13rWrBuIUssqcpLU')
#using the first tab of sheet
worksheet = wks.get_worksheet(0)
#Thaks to https://www.linkedin.com/pulse/manipulando-planilhas-do-google-usando-python-renan-pessoa/?originalSubdomain=pt
#And of course the official gspread documentation https://docs.gspread.org/en/latest/oauth2.html#enable-api-access
fullWorksheetValues = worksheet.get_all_values()

def getStudentsList(listOfLists):
    return listOfLists[3:]

def getStudentsResults(studentsList, totalClasses):
    #defining the result: the students list below   
    students = []
    for student in studentsList:
        average = calculateAverage(student)
        situation = calculateSituation(totalClasses, student, average)

        finalScore = calculateFinalScore(student, average, situation)

        student[6] = situation
        student[7] = finalScore

        students.append(student)
    return students

def calculateSituation (totalClasses, student, average):
    situation = ''
    if shouldReproveByAbcense (totalClasses, student):
        situation = 'Reprovado por Falta'
    elif average < 5.0:
        situation = 'Reprovado por Nota'
    elif average >= 5.0 and average < 7.0:
        situation = 'Exame Final'
    else:
        situation = 'Aprovado'
    return situation
    
def calculateAverage(student):
    #division by 10 to get the scale from 0 to 10
    avg = ((float(student[3]) + float(student[4]) + float(student[5])) / 3) / 10 
    return avg

def getTotalClasses(cellWithTotalClasses):
    #there is a standard in the cell
    #and it is spliting this pattern by colon and one space 
    #to get just the number
    cellWithTotalClassesList = cellWithTotalClasses.split(": ")
    totalClasses = int(cellWithTotalClassesList[1])
    print('Total of classes is: ', totalClasses)
    return totalClasses
#will be reproved if the abcence > than 25% os frequency
def shouldReproveByAbcense(totalClasses, student):
    lowFrequency = (totalClasses * 0.25)
    abcense = (int(student[2]))
    reproved = abcense > lowFrequency
    return reproved

def calculateFinalScore(student, average, situation):
    finalScore = 0
    #ATENTION! IS NAF RIGHT??? it seems the description of formula was wrong
    #So i inferer that the NAF is the sum of scores
    #But if i'm wrong just updat NAF to 0
    naf = int(student[3]) + int(student[4]) + int(student[5])
    if situation == 'Exame Final':
        finalScore = (average + naf) / 2
        finalScore = math.ceil(finalScore)
    return finalScore 

#starting the business rule and getting the new students list
totalClasses = getTotalClasses(fullWorksheetValues[1][0])
initialStudentsList =  getStudentsList(fullWorksheetValues)

studentsList = getStudentsResults(
                initialStudentsList, 
                totalClasses)

#updating the worksheet with the result
for index, student in enumerate(studentsList, start=4):
    print('index = ', index, '; student = ', student)
    worksheet.update('G' + str(index) + ':H' + str(index), [student[6:]])
    time.sleep(1)

