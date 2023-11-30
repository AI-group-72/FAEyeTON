from Analise import read_csv_file, ParsedData
import csv


def test_1():
    print('Test1 \n Basic input, Parsing by dist, arg=0.1, Standard output to .csv')
    section = read_csv_file('TestSamples/sample_data1.csv')
    metrics = ParsedData()
    metrics.parse(section, 2, 0.1)
    metrics.calc_metrics()
    metrics.to_csv('sample_data1.csv', 'TestSamples/sample_output.csv')


def test_2():
    print('Test2 \n Basic input, Parsing by area, arg=1, Standard output to .xlsx by row')
    section = read_csv_file('TestSamples/sample_data1.csv')
    metrics = ParsedData()
    metrics.parse(section, 1, 1)
    metrics.calc_metrics()
    metrics.to_xls_by_row('sample_data1.csv', 'TestSamples/sample_output.xlsx')


def test_3():
    print('Test3 \n Basic input, Parsing by speed, arg=30, Standard output to .xlsx by updating')
    section = read_csv_file('TestSamples/sample_data1.csv')
    metrics = ParsedData()
    metrics.parse(section, 0, 30, 2.5)
    metrics.to_xls('test_data1', 'TestSamples/masterfile.xlsx')


def test_4():
    print('Test4 \n Wrong input, Parsing by dist, 0.1, Standard output to .csv')
    section = read_csv_file('TestSamples/nullname')
    metrics = ParsedData()
    metrics.parse(section, 2, 0.1)
    metrics.to_csv('sample_data1.csv', 'TestSamples/sample_output.csv')


def test_5():
    print('Test5 \n Basic input, Parsing by dist, 0.1, Wrong output to .xlsx')
    section = read_csv_file('TestSamples/sample_data1.csv')
    metrics = ParsedData()
    metrics.parse(section, 2, 0.1)
    metrics.to_csv('sample_data1.csv', 'TestSamples/nullname.xlsx')


def test_6():
    print('Test6 \n Basic input, Parsing by dist, arg=0.1, Standard output to .csv')

    print('Comparing results')
    section = read_csv_file('TestSamples/sample_data1.csv')
    metrics = ParsedData()
    metrics.parse(section, 2, 0.1)
    metrics.calc_metrics()
    metrics.to_csv('sample_data1.csv', 'TestSamples/sample_output.csv')
    # compare with

    reader_last = csv.reader(open('TestSamples/sample_output.csv', newline=''), delimiter=',')
    data_last = []
    reader_standard = csv.reader(open('TestSamples/standard.csv', newline=''), delimiter=',')
    data_standard = []
    for row in reader_last:
        data_last = row
    for row in reader_standard:
        data_standard = row

    '''
    print(data_last)
    print(data_standard)
    '''

    fl = len(data_last) == len(data_standard)
    for i in range(0, len(data_last)):
        fl = fl and (data_last[i] == data_standard[i])
    print(fl)


test_6()
