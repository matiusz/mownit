#include <stdio.h>
#include <stdlib.h>
#include <gsl/gsl_blas.h>
#include <time.h>

int main(void)
{	
	clock_t t; 
	double time_taken;
	printf("Size,Mode,Time\r\n");
	for (int i = 101; i<1100; i=i+100)
	{
		for(int j=0;j<10;j++)
		{

			t = clock();
			test_matrix_x_matrix_naive(i);
			t = clock() - t; 
			time_taken = ((double)t)/CLOCKS_PER_SEC;
			printf("%i,%i,%g\r\n", i, 1, time_taken);
			t = clock();
			test_matrix_x_matrix_better(i);
			t = clock() - t; 
			time_taken = ((double)t)/CLOCKS_PER_SEC;
			printf("%i,%i,%g\r\n", i, 2, time_taken);
			t = clock();
			test_matrix_x_matrix_blas(i);
			t = clock() - t; 
			time_taken = ((double)t)/CLOCKS_PER_SEC;
			printf("%i,%i,%g\r\n", i, 3, time_taken);
		}
	}
	return 0;
}


int test_matrix_x_matrix_naive (int num)
{
	double *arr2d_1 = (double *)malloc(num * num * sizeof(double));
	double *arr2d_2 = (double *)malloc(num * num * sizeof(double));
	double *c = (double *)malloc(num * num * sizeof(double));
	int i, j, k;
	for (i = 0; i < num; i++)
	{
		for (j = 0; j < num; j++)
		{		
			*(arr2d_1 + i*num + j) = i + j;
			*(arr2d_2 + i*num + j) = i + j;
		}
	}
	for (i = 0; i < num; i++)
	{
		for (j = 0; j < num; j++)
		{	
			for (k = 0; k<num; k++)
			{	
			*(c + i*num + j) = *(c + i*num + j) + (*(arr2d_2 + k*num + j) * *(arr2d_1 + i*num + k));
			}
		}
	}
	free(arr2d_2);
	free(arr2d_1);
	free(c);
	return 0;
}

int test_matrix_x_matrix_better (int num)
{
	double *arr2d_1 = (double *)malloc(num * num * sizeof(double));
	double *arr2d_2 = (double *)malloc(num * num * sizeof(double));
	double *c = (double *)malloc(num * num * sizeof(double));
	int i, j, k;
	for (i = 0; i < num; i++)
	{
		for (j = 0; j < num; j++)
		{		
			*(arr2d_1 + i*num + j) = i + j;
			*(arr2d_2 + i*num + j) = i + j;
		}
	}
	for (i = 0; i < num; i++)
	{
		for (j = 0; j < num; j++)
		{	
			for (k = 0; k<num; k++)
			{	
			*(c + j*num + i) = *(c + j*num + i) + (*(arr2d_2 + k*num + j) * *(arr2d_1 + i*num + k));
			}
		}
	}
	free(arr2d_2);
	free(arr2d_1);
	free(c);
	return 0;
}


int test_matrix_x_matrix_blas (int num)
{
	double *arr2d_1 = (double *)malloc(num * num * sizeof(double));
	double *arr2d_2 = (double *)malloc(num * num * sizeof(double));
	int i, j;
	for (i = 0; i < num; i++)
	{
		for (j = 0; j < num; j++)
		{		
			*(arr2d_1 + i*num + j) = i + j;
			*(arr2d_2 + i*num + j) = i + j;
		}
	}


  double *c = (double *)malloc(num * num * sizeof(double));

  gsl_matrix_view A = gsl_matrix_view_array(arr2d_1, num, num);
  gsl_matrix_view B = gsl_matrix_view_array(arr2d_2, num, num);
  gsl_matrix_view C = gsl_matrix_view_array(c, num, num);

  gsl_blas_dgemm (CblasNoTrans, CblasNoTrans,
                  1.0, &A.matrix, &B.matrix,
                  0.0, &C.matrix);

	free(arr2d_2);
	free(arr2d_1);
	free(c);
	return 0;
}
