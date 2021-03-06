# --------------------------------------------------------------------------
# -----------------------  Rozpoznawanie Obrazow  --------------------------
# --------------------------------------------------------------------------
#  Zadanie 1: Regresja liniowa
#  autorzy: A. Gonczarek, J. Kaczmar, S. Zareba, P. Dąbrowski
#  2018
# --------------------------------------------------------------------------

import numpy as np

from utils import polynomial


def mean_squared_error(x, y, w):
    """
    :param x: ciag wejsciowy Nx1
    :param y: ciag wyjsciowy Nx1
    :param w: parametry modelu (M+1)x1
    :return: blad sredniokwadratowy pomiedzy wyjsciami y
    oraz wyjsciami uzyskanymi z wielowamiu o parametrach w dla wejsc x
    """
    y_pred = polynomial(x, w) #wektor predykcji dla danych wejściowych
    sub_vect = np.subtract(y_pred, y) #różnica wartość oczekiwana - wartość otrzymana
    sq_vect = np.square(sub_vect) #kwadrat różnicy
    err = np.mean(sq_vect) #średnia arytmetyczna kwadratów
    return err


def design_matrix(x_train, M):
    """
    :param x_train: ciag treningowy Nx1
    :param M: stopien wielomianu 0,1,2,...
    :return: funkcja wylicza Design Matrix Nx(M+1) dla wielomianu rzedu M
    """
    des_matrix = np.empty([len(x_train), M+1], float)
    for i in range(len(x_train)):#range(n) generuje listę [0, 1, ... n-1] - nie trzeba ręcznie zadawać tego n-1!!!
        for j in range(M+1):
            des_matrix[i][j] = pow(x_train[i], (j))
    return des_matrix


def least_squares(x_train, y_train, M):
    """
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param M: rzad wielomianu
    :return: funkcja zwraca krotke (w,err), gdzie w sa parametrami dopasowanego wielomianu, a err blad sredniokwadratowy
    dopasowania
    """
    #wzór (2)
    des_matrix = design_matrix(x_train, M)
    des_matrix_trans = des_matrix.transpose()
    dm_product = np.matmul(des_matrix_trans, des_matrix)
    dm_product_inverse = np.linalg.inv(dm_product)
    product = np.matmul(dm_product_inverse, des_matrix_trans)
    parameters = np.matmul(product, y_train) #wektor w to parameters
    err = mean_squared_error(x_train, y_train, parameters)
    return parameters, err


def regularized_least_squares(x_train, y_train, M, regularization_lambda):
    """
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param M: rzad wielomianu
    :param regularization_lambda: parametr regularyzacji
    :return: funkcja zwraca krotke (w,err), gdzie w sa parametrami dopasowanego wielomianu zgodnie z kryterium z regularyzacja l2,
    a err blad sredniokwadratowy dopasowania
    """
    # wzór (4)
    des_matrix = design_matrix(x_train, M)
    des_matrix_trans = des_matrix.transpose()
    identity_matrix = np.identity(M+1)
    dm_product = np.matmul(des_matrix_trans, des_matrix)
    sum_of_matrices = dm_product + regularization_lambda*identity_matrix
    dm_product_inverse = np.linalg.inv(sum_of_matrices)
    product = np.matmul(dm_product_inverse, des_matrix_trans)
    parameters = np.matmul(product, y_train)  # wektor w to parameters
    err_no_reg = mean_squared_error(x_train, y_train, parameters)
    return parameters, err_no_reg

def model_selection(x_train, y_train, x_val, y_val, M_values):
    """
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param x_val: ciag walidacyjny wejscia Nx1
    :param y_val: ciag walidacyjny wyjscia Nx1
    :param M_values: tablica stopni wielomianu, ktore maja byc sprawdzone
    :return: funkcja zwraca krotke (w,train_err,val_err), gdzie w sa parametrami modelu, ktory najlepiej generalizuje dane,
    tj. daje najmniejszy blad na ciagu walidacyjnym, train_err i val_err to bledy na sredniokwadratowe na ciagach treningowym
    i walidacyjnym
    """
    i = 0
    for M in M_values:
        parameters, train_err = least_squares(x_train, y_train, M)
        val_err = mean_squared_error(x_val, y_val, parameters)
        result = (parameters, train_err, val_err)
        if i == 0:
            best_result = result
        else:
            if result[2] < best_result[2]:
                best_result = result
        i += 1
    print("Best result error:", best_result[1])
    return best_result

def regularized_model_selection(x_train, y_train, x_val, y_val, M, lambda_values):
    """
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param x_val: ciag walidacyjny wejscia Nx1
    :param y_val: ciag walidacyjny wyjscia Nx1
    :param M: stopien wielomianu
    :param lambda_values: lista ze wartosciami roznych parametrow regularyzacji
    :return: funkcja zwraca krotke (w,train_err,val_err,regularization_lambda), gdzie w sa parametrami modelu, ktory najlepiej generalizuje dane,
    tj. daje najmniejszy blad na ciagu walidacyjnym. Wielomian dopasowany jest wg kryterium z regularyzacja. train_err i val_err to
    bledy na sredniokwadratowe na ciagach treningowym i walidacyjnym. regularization_lambda to najlepsza wartosc parametru regularyzacji
    """
    i = 0
    for lambda_val in lambda_values:
        parameters, train_err = regularized_least_squares(x_train, y_train, M, lambda_val)
        val_err = mean_squared_error(x_val, y_val, parameters)
        result = (parameters, train_err, val_err, lambda_val)
        if i == 0:
            best_result = result
        else:
            if result[2] < best_result[2]:
                best_result = result
        i += 1
    print("Best result error:", best_result[1])
    return best_result