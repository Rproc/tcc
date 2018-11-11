import numpy as np
from source import metrics
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from source.util import utils
import matplotlib as mpl


def plotAcc(data_acc, steps, label):
    data_acc = np.multiply(data_acc[0], 100)
    # print(data_acc)
    c = range(len(data_acc))
    # print(c)
    fig = plt.figure()
    fig.add_subplot(122)
    ax = plt.axes()
    ax.plot(c, data_acc, 'k')
    plt.yticks(range(0, 101, 10))
    plt.xticks(range(0, steps+1, 10))
    plt.title(label)
    plt.ylabel("Acurácia")
    plt.xlabel("Step")
    plt.grid()
    plt.show()

def plotTime(listOfTimes, listOfMethods):

    for l in range(len(listOfTimes)):
        ax = plt.axes()
        ax.bar(l, listOfTimes[l], label=listOfMethods[l], align='center', width=0.4)

    # fig = plt.figure(figsize=(1,1))
    plt.title("Tempo de processamento para toda a stream")
    plt.legend(listOfMethods)
    plt.xlabel("Métodos")
    plt.ylabel("Tempo de Execução")
    plt.xticks(range(len(listOfTimes)))
    plt.show()

def plotAverageAcc(listOfAcc, listOfMethods):

    listOfAcc = np.multiply(listOfAcc, 100)

    for l in range(len(listOfAcc)):
        ax = plt.axes()
        ax.bar(l, listOfAcc[l], align='center', width=0.4)

    plt.title("Acurácia Média")
    plt.xlabel("Métodos")
    plt.ylabel("Acurácia")
    plt.yticks(range(0, 101, 10))
    plt.xticks(range(len(listOfAcc)), listOfMethods)
    plt.xticks(rotation=90)
    plt.grid()
    plt.show()

def plotAccuracyCurves(listOfAccuracies, listOfMethods):
    limit = len(listOfAccuracies[0])+1
    listOfAccuracies = np.multiply(listOfAccuracies, 100)
    for acc in listOfAccuracies:
        acc = np.array(acc)
        c = range(len(acc))
        ax = plt.axes()
        ax.plot(c, acc)

    plt.title("Curva de Acurácia")
    plt.legend(listOfMethods, loc=3)
    plt.yticks([0,10,20,30,40,50,60,70,80,90,100])
    plt.xticks(range(0, limit, 10))
    plt.ylabel("Acurácia")
    plt.xlabel("Step")
    plt.grid()
    plt.show()

def plotBoxplot(mode, data, labels):
    fig = plt.figure()
    fig.add_subplot(111)
    plt.boxplot(data, labels=labels)
    plt.xticks(rotation=90)

    if mode == 'acc':
        plt.title("Acurácia - Boxplot")
        #plt.xlabel('step (s)')
        plt.ylabel('Acurácia')
    elif mode == 'mcc':
        plt.title('Mathews Correlation Coefficient - Boxplot')
        plt.ylabel("Mathews Correlation Coefficient")
    elif mode == 'f1':
        plt.title('Macro-F1 - Boxplot')
        plt.ylabel("Macro-F1")

    plt.show()

def plotF1(arrF1, steps, label):
    arrF1 = np.array(arrF1)
    c = range(len(arrF1))
    fig = plt.figure()
    fig.add_subplot(122)
    ax = plt.axes()
    ax.plot(c, arrF1, 'k')
    plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    if steps > 10:
        plt.xticks(range(1, steps+1, 10))
    else:
        plt.xticks(range(1, steps+1))
    plt.title(label)
    plt.ylabel("F1")
    plt.xlabel("Step")
    plt.grid()
    plt.show()

def plotPerBatches(stream, predicted, actualLabel, size_stream):

    # 2 Classes, 2 features
    if len(stream[0,:-1]) == 2 and len(list(set(actualLabel))) == 2:
        for i in range(0, 100):
            classes = list(set(actualLabel))
            # print(classes)
            plt.rcParams["figure.figsize"] = (10.5,4.8)
            fig = plt.figure()
            cmx = plt.get_cmap('Paired')
            colors = ['lightskyblue', 'mediumseagreen']#cmx(np.linspace(0, 1, (len(classes)*2)+1))
            handles = []
            classLabels = []
            color = 0
            ax = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            handles2 = []

            newlist_original = actualLabel[int((i/100)*size_stream):int(((i+1)/100)*size_stream)]
            newlist_predicted = predicted[int((i/100)*size_stream):int(((i+1)/100)*size_stream)]
            batch = stream[int((i/100)*size_stream):int(((i+1)/100)*size_stream), :-1]

            for cl in classes:
                color = int(cl) - 1
                # print(color)
                p = batch[np.where(newlist_original==cl)[0]]
                p2 = batch[np.where(newlist_predicted==cl)[0]]
                x1 = p[:,0]
                x2 = p[:,1]

                pred1 = p2[:, 0]
                pred2 = p2[:, 1]
                handles.append(ax.scatter(x1, x2, c = colors[color], alpha=0.7))
                handles2.append(ax2.scatter(pred1, pred2, c = colors[color], alpha=0.7))
                color+=1
                classLabels.append('Class {}'.format(cl))



            ax.legend(handles, classLabels)
            ax.set_title('Rótulos reais')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax2.legend(handles2, classLabels)
            ax2.set_title('Rótulos do Handshake')
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            title = "Distribuição dos dados. Step {}".format(i)
            fig.suptitle(title)
            plt.show()

    # 2 Classes, n features --- NOAA, elec
    elif len(stream[0,:-1]) > 2 and len(list(set(actualLabel))) == 2:

        stream = u.pca(stream, 2)

        for i in range(0, 100):
            classes = list(set(actualLabel))
            # print(classes)
            plt.rcParams["figure.figsize"] = (10.5,4.8)
            fig = plt.figure()
            cmx = plt.get_cmap('Paired')
            colors = ['lightskyblue', 'mediumseagreen']#cmx(np.linspace(0, 1, (len(classes)*2)+1))
            handles = []
            classLabels = []
            color = 0
            ax = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            handles2 = []

            newlist_original = actualLabel[int((i/100)*size_stream):int(((i+1)/100)*size_stream)]
            newlist_predicted = predicted[int((i/100)*size_stream):int(((i+1)/100)*size_stream)]
            batch = stream[int((i/100)*size_stream):int(((i+1)/100)*size_stream), :-1]

            for cl in classes:
                color = int(cl) - 1
                # print(color)
                p = batch[np.where(newlist_original==cl)[0]]
                p2 = batch[np.where(newlist_predicted==cl)[0]]
                x1 = p[:,0]
                x2 = p[:,1]

                pred1 = p2[:, 0]
                pred2 = p2[:, 1]
                handles.append(ax.scatter(x1, x2, c = colors[color], alpha=0.7))
                handles2.append(ax2.scatter(pred1, pred2, c = colors[color], alpha=0.7))
                color+=1
                classLabels.append('Class {}'.format(cl))



            ax.legend(handles, classLabels)
            ax2.legend(handles2, classLabels)
            title = "Distribuição dos dados. Step {}".format(i)
            fig.suptitle(title)
            plt.show()

    # n classes, n features ---- keystroke
    elif len(stream[0,:-1]) > 2 and len(list(set(actualLabel))) > 2:

        stream = u.pca(stream, 2)

        for i in range(0, 100):
            classes = list(set(actualLabel))
            # print(classes)
            plt.rcParams["figure.figsize"] = (10.5,4.8)
            fig = plt.figure()
            cmx = plt.get_cmap('Paired')
            colors = ['lightskyblue', 'mediumseagreen', 'orange', 'darkmagenta']#cmx(np.linspace(0, 1, (len(classes)*2)+1))
            handles = []
            classLabels = []
            color = 0
            ax = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            handles2 = []

            newlist_original = actualLabel[int((i/100)*size_stream):int(((i+1)/100)*size_stream)]
            newlist_predicted = predicted[int((i/100)*size_stream):int(((i+1)/100)*size_stream)]
            batch = stream[int((i/100)*size_stream):int(((i+1)/100)*size_stream), :-1]

            for cl in classes:
                color = int(cl) - 1
                # print(color)
                p = batch[np.where(newlist_original==cl)[0]]
                p2 = batch[np.where(newlist_predicted==cl)[0]]
                x1 = p[:,0]
                x2 = p[:,1]

                pred1 = p2[:, 0]
                pred2 = p2[:, 1]
                handles.append(ax.scatter(x1, x2, c = colors[color], alpha=0.7))
                handles2.append(ax2.scatter(pred1, pred2, c = colors[color], alpha=0.7))
                color+=1
                classLabels.append('Class {}'.format(cl))



            ax.legend(handles, classLabels)
            ax2.legend(handles2, classLabels)
            title = "Distribuição dos dados. Step {}".format(i)
            fig.suptitle(title)
            plt.show()

def plot(X, y, t):
    classes = list(set(y))
    fig = plt.figure()
    handles = []
    classLabels = []
    cmx = plt.get_cmap('Paired')
    colors = cmx(np.linspace(0, 1, (len(classes)*2)+1))
    #classLabels = ['Class 1', 'Core 1', 'Class 2', 'Core 2']
    color=0
    for cl in classes:
        #points
        points = X[np.where(y==cl)[0]]
        x1 = points[:,0]
        x2 = points[:,1]
        handles.append(ax.scatter(x1, x2, c = colors[color]))
        #core support points
        color+=1
        corePoints = coreX[np.where(coreY==cl)[0]]
        coreX1 = corePoints[:,0]
        coreX2 = corePoints[:,1]
        handles.append(ax.scatter(coreX1, coreX2, c = colors[color]))
        #labels
        classLabels.append('Class {}'.format(cl))
        classLabels.append('Core {}'.format(cl))
        color+=1

    ax.legend(handles, classLabels)
    title = "Data distribution. Step {}".format(t)
    plt.title(title)
    plt.show()
