#include <stdio.h>
#include <stdlib.h>
#include <gsl/gsl_blas.h>
#include <time.h>

int main(void)
{	
	clock_t t; 
	double time_taken_v_v;
	double time_taken_m_v;
	printf("size,try_no,vector*vector,vector*matrix\n");
	for (int i = 1; i<10000; i=i+100)
	{
		for(int j=0;j<10;j++)
		{
			t = clock();
			test_vector_x_vector(i);
			t = clock() - t; 
			time_taken_v_v = ((double)t)/CLOCKS_PER_SEC;
			t = clock();
			test_matrix_x_vector(i);
			t = clock() - t; 
			time_taken_m_v = ((double)t)/CLOCKS_PER_SEC;
			printf("%d,%d,%f,%f\n", i, j, time_taken_v_v, time_taken_m_v);
		}
	}
	return 0;
}


int test_vector_x_vector(int num)
{
	double *arr1d_1 = malloc(num * sizeof(double));
	double *arr1d_2 = malloc(num * sizeof(double));
	int i, j;
	for (i = 0; i < num; i++)
	{
		arr1d_1[i]=i;
		arr1d_2[i]=num-i;
	}


  double c;

  gsl_vector_view A = gsl_vector_view_array(arr1d_1, num);
  gsl_vector_view B = gsl_vector_view_array(arr1d_2, num);

  gsl_blas_ddot(&A.vector, &B.vector, &c);


	free(arr1d_1);
	free(arr1d_2);
	return 0;
}


int test_matrix_x_vector (int num)
{
	double *arr2d_1 = (double *)malloc(num * num * sizeof(double));
	double *arr1d_1 = malloc(num * sizeof(double));
	int i, j;
	for (i = 0; i < num; i++)
	{
		for (j = 0; j < num; j++)
		{		
			*(arr2d_1 + i*num + j) = i + j; 
		}
		arr1d_1[i]=i;
	}


  double *c = malloc(num * sizeof(double));

  gsl_matrix_view A = gsl_matrix_view_array(arr2d_1, num, num);
  gsl_vector_view B = gsl_vector_view_array(arr1d_1, num);
  gsl_vector_view C = gsl_vector_view_array(c, num);

  gsl_blas_dgemv (CblasNoTrans, 
                  1.0, &A.matrix, &B.vector,
                  1.0, &C.vector);


	free(arr1d_1);
	free(arr2d_1);
	free(c);
	return 0;
}
