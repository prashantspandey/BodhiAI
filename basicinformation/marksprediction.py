import numpy as np
import pickle
from datetime import datetime, date
from basicinformation.models import Subject

'''
load pickles for data transformation and prediction (hindi)
'''
pickle_in_hindi = open('F:\\bodhi.ai\\bodhialgorithms\\preprocesshindihy.pickle', 'rb')
svm_pickle_hindi = open('F:\\bodhi.ai\\bodhialgorithms\\svmhindihhy.pickle', 'rb')
sca_hindi = pickle.load(pickle_in_hindi)
svmhindihhy = pickle.load(svm_pickle_hindi)

'''
load pickles for data transformation and prediction (maths)
'''
pickle_in_maths = open('F:\\bodhi.ai\\bodhialgorithms\\preprocesshindihy.pickle', 'rb')
knn7_pickle_maths = open('F:\\bodhi.ai\\bodhialgorithms\\svmhindihhy.pickle', 'rb')
sca_maths = pickle.load(pickle_in_maths)
knn7mathshhy = pickle.load(knn7_pickle_maths)

'''
load pickles for data transformation and prediction (english)
'''
pickle_in_english = open('F:\\bodhi.ai\\bodhialgorithms\\preprocesshindihy.pickle', 'rb')
knn7_pickle_english = open('F:\\bodhi.ai\\bodhialgorithms\\svmhindihhy.pickle', 'rb')
sca_english = pickle.load(pickle_in_english)
knn7englishhhy = pickle.load(knn7_pickle_english)

'''
load pickles for data transformation and prediction (science)
'''
pickle_in_science = open('F:\\bodhi.ai\\bodhialgorithms\\preprocesshindihy.pickle', 'rb')
knn7_pickle_science = open('F:\\bodhi.ai\\bodhialgorithms\\svmhindihhy.pickle', 'rb')
sca_science = pickle.load(pickle_in_science)
knn7sciencehhy = pickle.load(knn7_pickle_science)


# test1,test2,test3,age,section
# x = np.array([[9, 10, 10, 12, 1]])
# x = sca.transform(x)
# print(x)
# prd = svmhindihhy.predict(x)
# print(prd)


def hindi_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
    calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)
    # age = int((date.today() - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_hindi.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = svmhindihhy.predict(overall)
    return prediction


def maths_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
        calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_maths.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7mathshhy.predict(overall)
    return prediction


def english_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
        calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_english.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7englishhhy.predict(overall)
    return prediction


def science_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

        '''
            calculate age using DOB (dd/mm/year)
        '''
    days_in_year = 365.2425

    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_science.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7sciencehhy.predict(overall)
    return prediction


def predictionConvertion(prediction):
    if prediction == 0:
        conversion = '<40% '
    elif prediction == 1:
        conversion = '40% - 50% '
    elif prediction == 2:
        conversion = '50% - 60% '
    elif prediction == 3:
        conversion = '60% - 70%'
    elif prediction == 4:
        conversion = '70%-80% '
    elif prediction == 5:
        conversion = '80%-90% '
    elif prediction == 6:
        conversion = '90%-100% '
    else:
        conversion = 'something wrong'
    return conversion

# function for updating all the half yearly predictions (whole database)
def update_all_predictedmarks():
    subject = Subject.objects.all()
    alluniquestudents = set()
    sub = []
    for i in subject:
        alluniquestudents.add(i.student)
    allsubjects = []
    for j in alluniquestudents:
        allsubjects.extend(j.subject_set.all())

    for thisSubject in allsubjects:
        if thisSubject.name == 'Hindi':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                hindi_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                        thisSubject.student.dob, section))

            thisSubject.save()
        elif thisSubject.name == 'English':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                english_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                          thisSubject.student.dob, section))
            thisSubject.save()

        elif thisSubject.name == 'Maths':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                maths_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                        thisSubject.student.dob, section))
            thisSubject.save()

        elif thisSubject.name == 'Science':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                science_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                          thisSubject.student.dob, section))
            thisSubject.save()

        else:
            pass
