//
// Created by wiktor on 12/10/16.
//

#include "headers.h"

double **data_1;
double **data_2;
double **data_3;
double **data_4;
FILE* stats;

int eps = 0;
#define LEFT_POSITION 0;
#define ON_POSITION 1;
#define RIGHT_POSITION 2;

char * positions[3] = {"LEFT", "ON", "RIGHT"};
FILE* get_file_handler(char* file_name, char *access) {
    FILE* file = fopen(file_name, access);
    if(file == NULL) {
        printf("Cannot open file: %s.\n", file_name);
        exit(1);
    }
}

char* get_file_name(char* file_path, int algorithm, char* type) {
    char* path = calloc(strlen(file_path), sizeof(char));
    char* alg_in_string = calloc(1, sizeof(char));
    sprintf(alg_in_string, "%d", algorithm);
    if(path == NULL) {
        printf("Memory allocation error");
        exit(2);
    }
    

    strncpy(path, file_path, strlen(file_path));
    strcat(path, "_");
    strcat(path, alg_in_string);
    strcat(path, "_");
    strcat(path, type);
    strcat(path, ".csv");

    return path;
}

const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, " ");
            tok && *tok;
            tok = strtok(NULL, ";\n"))
    {
        if (!--num)
            return tok;
    }
    return NULL;
}

int read_into_arrays(char * file_name, double **array) {
    char buffer[255];
    FILE* ds1 = get_file_handler(file_name, "r");
        int j = 0;
        while(fgets(buffer, 255, (FILE*) ds1)) {
            const char* x = strtok(buffer, " ");
            const char* y = strtok(NULL, " ");
            array[0][j] = strtod(x, NULL);
            array[1][j] = strtod(y, NULL);
            j++; 
        }
    return 0;
}


double compute_det(double p_x0, double p_y0, double p_x1, 
    double p_y1, double p_x2, double p_y2, int alg) {
    double p0[] = {p_x0, p_y0};
    double p1[] = {p_x1, p_y1};
    double p2[] = {p_x2, p_y2};
     
    if (alg == 1) 
        return p_x0 * p_y1 + p_x1 * p_y2 + p_x2 * p_y0 - p_x1*p_y0 - p_x0*p_y2 - p_x2*p_y1; 
    else if (alg == 2)
        return orient2dfast(p0, p1, p2);
    else if (alg == 3)
        return orient2dexact(p0, p1, p2);
    else if (alg == 4)
        return orient2dslow(p0, p1, p2);
    return (p_x0 - p_x2) * (p_y1 - p_y2) - (p_y0 - p_y2) * (p_x1 - p_x2);
}

int compare_with_epsilon(double result) {
    int sign = result < 0 ? -1 : 1;
    result = result < 0 ? (-1) * result : result;

    if(result > eps) {
        if(sign == 1) {
            return GT;
        }
        else {
            return LT;
        }
    }

    return EQ;
}


int map_equality_to_position(int equality) {
    return ++equality;
}

int classify_by_data(char * file_path, double **data, int len) {
    double *x_points = data[0];
    double *y_points = data[1];

    char * file_name;
    FILE* inconsistent_points = get_file_handler((file_name = get_file_name(file_path, 0, "")), "w");
    free(file_name);

    for(int j = 0; j < len; j++) {
        double a_x = -1, a_y = 0, b_x = 1, b_y = 0.1;
        double derivative1 = compute_det(a_x, a_y, b_x, b_y, x_points[j], y_points[j], 0);
        double derivative2 = compute_det(a_x, a_y, b_x, b_y, x_points[j], y_points[j], 1);
        double fast = compute_det(a_x, a_y, b_x, b_y, x_points[j], y_points[j], 2);
        double exact = compute_det(a_x, a_y, b_x, b_y, x_points[j], y_points[j], 3);
        double slow = compute_det(a_x, a_y, b_x, b_y, x_points[j], y_points[j], 4);

        int algNumber = 5;
        int results[algNumber];

        results[0] = compare_with_epsilon(derivative1);
        results[1] = compare_with_epsilon(derivative2);
        results[2] = compare_with_epsilon(fast);
        results[3] = compare_with_epsilon(exact);
        results[4] = compare_with_epsilon(slow);

        int result_count[3];
        for (int i = 0; i < 3; i++) {
            result_count[i] = 0;
        }
        for(int i = 0; i < algNumber; i++) {
            result_count[map_equality_to_position(results[i])]++;
        }

        for (int i = 0; i < 3; i++) {
            if(result_count[i] != 0 && result_count[i] != algNumber) {
                fprintf(inconsistent_points, "%.15lf %.15lf %s %s %s %s %s\n",
                        x_points[j],
                        y_points[j],
                        positions[map_equality_to_position(results[0])],
                        positions[map_equality_to_position(results[1])],
                        positions[map_equality_to_position(results[2])],
                        positions[map_equality_to_position(results[3])],
                        positions[map_equality_to_position(results[4])]
                );

                break;
            }
        }

    }
}


int classify(char * file_path, double **data, int len) {
    for(int i = 0; i < 5; i++) {
        char * file_name;


        FILE* on = get_file_handler((file_name = get_file_name(file_path, i, "o")), "w");
        free(file_name);
        FILE* left = get_file_handler((file_name = get_file_name(file_path, i, "l")), "w");
        free(file_name);
        FILE* right = get_file_handler((file_name = get_file_name(file_path, i, "r")), "w");   
        free(file_name);



        clock_t start = clock();

        double a_x = -1, a_y = 0, b_x = 1, b_y = 0.1;
        double x, y;
        int mistakes = 0;
        int left_count = 0, right_count = 0, on_count = 0;

        double *x_points = data[0];
        double *y_points = data[1];

        for(int j = 0; j < len; j++) {
            double res = compute_det(a_x, a_y, b_x, b_y, x_points[j], y_points[j], i);

            double y_coord = 0.05 * x_points[j] + 0.05;
            double diff = y_points[j] - y_coord;

            int real = compare_with_epsilon(diff);
            int det = compare_with_epsilon(res);

            if(real != det) {
                mistakes++;
            }

            if(det == GT) {
                left_count++;
                fprintf(left, "%.15lf %.15lf\n", x_points[j], y_points[j]);
            }
            else if(det == LT) {
                right_count++;
                fprintf(right, "%.15lf %.15lf\n", x_points[j], y_points[j]);
            }
            else {
                on_count++;
                fprintf(on, "%.15lf %.15lf\n", x_points[j], y_points[j]);
            }
        }
        file_name = get_file_name(file_path, i, "");
        fprintf(stats, "%s; %d; %d; %d;\n", file_name, left_count, on_count, right_count);
        free(file_name);

        clock_t end = clock();

        printf("Algorithm %d with data_set_%s.csv took: %.2f miliseconds.\n", i, file_path, (float)(end - start) / CLOCKS_PER_SEC * 1000);
        printf("Number of mistakes: %d\n", mistakes);
    

        fclose(on);
        fclose(left);
        fclose(right);
    }
}

double ** init_array(double **array, int cols) {
    array = malloc(2 * sizeof *array);
    for (int i=0; i<2; i++) {
        array[i] = malloc((cols+1) * sizeof *array[i]);
    }
    return array;
}

int main(int argc, char **argv) {
    exactinit();
    data_1 = init_array(data_1, 100000);
    data_2 = init_array(data_2, 100000);
    data_3 = init_array(data_3, 1000);
    data_4 = init_array(data_4, 1000);
    stats = get_file_handler("stats", "w+");
    fprintf(stats, "alg; left; on; right;\n");
      
    read_into_arrays("data_set_1.csv", data_1);
    read_into_arrays("data_set_2.csv", data_2);
    read_into_arrays("data_set_3.csv", data_3);
    read_into_arrays("data_set_4.csv", data_4);

    printf("Epsilon 0\n");
    classify("1", data_1, 100000);
    classify("2", data_2, 100000);
    classify("3", data_3, 1000);
    classify("4", data_4, 1000);

    printf("Epsilon 6\n");
    eps = 1e-6;
    classify("1", data_1, 100000);
    classify("2", data_2, 100000);
    classify("3", data_3, 1000);
    classify("4", data_4, 1000);

    printf("Epsilon 12\n");
    eps = 1e-12;
    classify("1", data_1, 100000);
    classify("2", data_2, 100000);
    classify("3", data_3, 1000);
    classify("4", data_4, 1000);

    classify_by_data("1_inconsistent", data_1, 100000);
    classify_by_data("2_inconsistent", data_2, 100000);
    classify_by_data("3_inconsistent", data_3, 1000);
    classify_by_data("4_inconsistent", data_4, 1000);
    free(data_1);
    free(data_2);
    free(data_3);
    free(data_4);
    // free(stats);
    return 0;
}