/*
 * Author: Ivan Temesvari
 * Date: 5/21/2024
 * This is a dynamic divide-and-conquer parallel multiplication algorithm.
 * This program uses parallel schemes for concurrency to compute
 * the product of large integers.
 *
 */

#include <iostream>
#include <cmath>
#include <thread>
#include <vector>
#include <omp.h>
#include <gmpxx.h>
#include <future>
#include <chrono>

// Function to perform multiplication.
mpz_class mult(const mpz_class &x, const mpz_class &y){
	 // Find number of digits of x and y
	int len_x = mpz_sizeinbase(x.get_mpz_t(), 10);
	int len_y = mpz_sizeinbase(y.get_mpz_t(), 10);
	mpz_class result;

	if (x < 10 || y < 10) {
		return x * y;
	} else {
		// Create temporary mpz_t variables for powers of 10
		mpz_t pow10_x, pow10_y;
		mpz_init(pow10_x);
		mpz_init(pow10_y);

		// Calculate powers of 10
		//len_x - len_x / 2
		mpz_pow_ui(pow10_x, mpz_class("10").get_mpz_t(), int(len_x / 2));
		mpz_pow_ui(pow10_y, mpz_class("10").get_mpz_t(), int(len_y / 2));

		// Divide up each number into four products
		mpz_class x1 = x / mpz_class(pow10_x);
		mpz_class x2 = x % mpz_class(pow10_x);
		mpz_class y1 = y / mpz_class(pow10_y);
		mpz_class y2 = y % mpz_class(pow10_y);

		// Clear temporary mpz_t variables
		mpz_clear(pow10_x);
		mpz_clear(pow10_y);

		mpz_class pow10_x1_y1;
		mpz_class pow10_x1_y2;
		mpz_class pow10_y1_x2;

		mpz_init(pow10_x1_y1.get_mpz_t());
		mpz_init(pow10_x1_y2.get_mpz_t());
		mpz_init(pow10_y1_x2.get_mpz_t());
		mpz_pow_ui(pow10_x1_y1.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2) + int(len_y / 2));
		mpz_pow_ui(pow10_x1_y2.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2));
		mpz_pow_ui(pow10_y1_x2.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_y / 2));

		return mult(x1, y1)*pow10_x1_y1
				+ mult(x1, y2)*pow10_x1_y2
				+ mult(x2, y2)
				+ mult(y1, x2)*pow10_y1_x2;
	}
}
// Function to perform multiplication using threads and GMP
void mult_threads_helper(const mpz_class &x, const mpz_class &y, mpz_class &result) {
    // Find number of digits of x and y
    int len_x = mpz_sizeinbase(x.get_mpz_t(), 10);
    int len_y = mpz_sizeinbase(y.get_mpz_t(), 10);

    if (x < 10 || y < 10) {
        result = x * y;
    } else {
    	// Create temporary mpz_t variables for powers of 10
		mpz_t pow10_x, pow10_y;
		mpz_init(pow10_x);
		mpz_init(pow10_y);

		// Calculate powers of 10
		//len_x - len_x / 2
		mpz_pow_ui(pow10_x, mpz_class("10").get_mpz_t(), int(len_x / 2));
		mpz_pow_ui(pow10_y, mpz_class("10").get_mpz_t(), int(len_y / 2));

		// Divide up each number into four products
        mpz_class x1 = x / mpz_class(pow10_x);
        mpz_class x2 = x % mpz_class(pow10_x);
        mpz_class y1 = y / mpz_class(pow10_y);
        mpz_class y2 = y % mpz_class(pow10_y);

        // Clear temporary mpz_t variables
        mpz_clear(pow10_x);
        mpz_clear(pow10_y);

        // Recursively call mult_threads_helper for each quadrant
        mpz_class P1, P2, P3, P4;
        std::thread t1(mult_threads_helper, std::cref(x1), std::cref(y1), std::ref(P1));
        std::thread t2(mult_threads_helper, std::cref(x1), std::cref(y2), std::ref(P2));
        std::thread t3(mult_threads_helper, std::cref(x2), std::cref(y2), std::ref(P3));
        std::thread t4(mult_threads_helper, std::cref(y1), std::cref(x2), std::ref(P4));

        // Join the threads to wait for their completion
        t1.join();
        t2.join();
        t3.join();
        t4.join();

        // Calculate the result using the obtained products
        mpz_class res = P1;
        mpz_class pow10;
        mpz_init(pow10.get_mpz_t());
        mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2) + int(len_y / 2));
        res *= pow10;
        mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2));
        res += P2 * pow10;
        res += P3;
        mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_y / 2));
        res += P4 * pow10;
        result = res;
    }
}

// Wrapper function to handle the result and call mult_threads_helper
mpz_class mult_threads_join(const mpz_class &x, const mpz_class &y) {
    mpz_class result;
    mult_threads_helper(x, y, result);
    return result;
}

// Function to perform multiplication using OpenMP
mpz_class mult_threads_omp(const mpz_class &x, const mpz_class &y) {
    // Find number of digits of x and y
    int len_x = mpz_sizeinbase(x.get_mpz_t(), 10);
    int len_y = mpz_sizeinbase(y.get_mpz_t(), 10);

    if (x < 10 || y < 10) {
        return x * y;
    } else {
    	// Create temporary mpz_t variables for powers of 10
		mpz_t pow10_x, pow10_y;
		mpz_init(pow10_x);
		mpz_init(pow10_y);

		// Calculate powers of 10
		//len_x - len_x / 2
		mpz_pow_ui(pow10_x, mpz_class("10").get_mpz_t(), int(len_x / 2));
		mpz_pow_ui(pow10_y, mpz_class("10").get_mpz_t(), int(len_y / 2));

		// Divide up each number into four products
        mpz_class x1 = x / mpz_class(pow10_x);
        mpz_class x2 = x % mpz_class(pow10_x);
        mpz_class y1 = y / mpz_class(pow10_y);
        mpz_class y2 = y % mpz_class(pow10_y);

        // Clear temporary mpz_t variables
        mpz_clear(pow10_x);
        mpz_clear(pow10_y);

        // Variables to store the partial results
        mpz_class P1, P2, P3, P4;

        // Use OpenMP parallel region to run the recursive calls in parallel
        #pragma omp parallel sections
        {
            #pragma omp section
            P1 = mult_threads_omp(x1, y1);

            #pragma omp section
            P2 = mult_threads_omp(x1, y2);

            #pragma omp section
            P3 = mult_threads_omp(x2, y2);

            #pragma omp section
            P4 = mult_threads_omp(y1, x2);
        }

        // Calculate the result using the obtained products
		mpz_class res = P1;
		mpz_class pow10;
		mpz_init(pow10.get_mpz_t());
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2) + int(len_y / 2));
		res *= pow10;
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2));
		res += P2 * pow10;
		res += P3;
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_y / 2));
		res += P4 * pow10;
		return res;
    }
}

// Function to perform multiplication using async and GMP
#include <iostream>
#include <future>
#include <gmpxx.h>

// Function to perform multiplication using async and GMP
mpz_class mult_threads_async(const mpz_class &x, const mpz_class &y) {
    // Find number of digits of x and y
    int len_x = mpz_sizeinbase(x.get_mpz_t(), 10);
    int len_y = mpz_sizeinbase(y.get_mpz_t(), 10);

    if (x < 10 || y < 10) {
        return x * y;
    } else {
    	// Create temporary mpz_t variables for powers of 10
		mpz_t pow10_x, pow10_y;
		mpz_init(pow10_x);
		mpz_init(pow10_y);

		// Calculate powers of 10
		//len_x - len_x / 2
		mpz_pow_ui(pow10_x, mpz_class("10").get_mpz_t(), int(len_x / 2));
		mpz_pow_ui(pow10_y, mpz_class("10").get_mpz_t(), int(len_y / 2));

		// Divide up each number into four products
		mpz_class x1 = x / mpz_class(pow10_x);
		mpz_class x2 = x % mpz_class(pow10_x);
		mpz_class y1 = y / mpz_class(pow10_y);
		mpz_class y2 = y % mpz_class(pow10_y);

		// Clear temporary mpz_t variables
		mpz_clear(pow10_x);
		mpz_clear(pow10_y);

        // Use async to run the recursive calls in parallel
        auto future_P1 = std::async(std::launch::async, mult_threads_async, x1, y1);
        auto future_P2 = std::async(std::launch::async, mult_threads_async, x1, y2);
        auto future_P3 = std::async(std::launch::async, mult_threads_async, x2, y2);
        auto future_P4 = std::async(std::launch::async, mult_threads_async, y1, x2);

        // Get the results from the futures
        mpz_class P1 = future_P1.get();
        mpz_class P2 = future_P2.get();
        mpz_class P3 = future_P3.get();
        mpz_class P4 = future_P4.get();

        // Calculate the result using the obtained products
		mpz_class res = P1;
		mpz_class pow10;
		mpz_init(pow10.get_mpz_t());
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2) + int(len_y / 2));
		res *= pow10;
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2));
		res += P2 * pow10;
		res += P3;
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_y / 2));
		res += P4 * pow10;
		return res;
    }
}

// Function to perform multiplication using async and GMP
mpz_class mult_threads_async_recursive(const mpz_class &x, const mpz_class &y) {
    // Find number of digits of x and y
    int len_x = mpz_sizeinbase(x.get_mpz_t(), 10);
    int len_y = mpz_sizeinbase(y.get_mpz_t(), 10);

    if (x < 10 || y < 10) {
        return x * y;
    } else {
    	// Create temporary mpz_t variables for powers of 10
		mpz_t pow10_x, pow10_y;
		mpz_init(pow10_x);
		mpz_init(pow10_y);

		// Calculate powers of 10
		//len_x - len_x / 2
		mpz_pow_ui(pow10_x, mpz_class("10").get_mpz_t(), int(len_x / 2));
		mpz_pow_ui(pow10_y, mpz_class("10").get_mpz_t(), int(len_y / 2));

		// Divide up each number into four products
		mpz_class x1 = x / mpz_class(pow10_x);
		mpz_class x2 = x % mpz_class(pow10_x);
		mpz_class y1 = y / mpz_class(pow10_y);
		mpz_class y2 = y % mpz_class(pow10_y);

		// Clear temporary mpz_t variables
		mpz_clear(pow10_x);
		mpz_clear(pow10_y);

        // Use async to run the recursive calls in parallel
        auto future_P1 = std::async(std::launch::async, mult, x1, y1);
        auto future_P2 = std::async(std::launch::async, mult, x1, y2);
        auto future_P3 = std::async(std::launch::async, mult, x2, y2);
        auto future_P4 = std::async(std::launch::async, mult, y1, x2);

        // Get the results from the futures
        mpz_class P1 = future_P1.get();
        mpz_class P2 = future_P2.get();
        mpz_class P3 = future_P3.get();
        mpz_class P4 = future_P4.get();

        // Calculate the result using the obtained products
		mpz_class res = P1;
		mpz_class pow10;
		mpz_init(pow10.get_mpz_t());
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2) + int(len_y / 2));
		res *= pow10;
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_x / 2));
		res += P2 * pow10;
		res += P3;
		mpz_pow_ui(pow10.get_mpz_t(), mpz_class("10").get_mpz_t(), int(len_y / 2));
		res += P4 * pow10;
		return res;
    }
}

int main() {
	// Example large numbers
	mpz_class x("9248723412123456124343243245325566545454358769219834539434523453426435");
	mpz_class y("6924126745567865434326657889774555534984502495486004038899837498372495");

	// Measure the time taken by the mult_threads function
	auto start = std::chrono::high_resolution_clock::now();
	// Perform multiplication
	mpz_class result = mult_threads_omp(x, y);
	auto end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = end - start;
	std::cout << "Result (omp): " << result.get_str() << std::endl;
	std::cout << "Time taken: " << elapsed.count() << " seconds" << std::endl;

	start = std::chrono::high_resolution_clock::now();
	result = mult_threads_async(x, y);
	end = std::chrono::high_resolution_clock::now();
	elapsed = end - start;
	std::cout << "Result (async-get-threads): " << result.get_str() << std::endl;
	std::cout << "Time taken: " << elapsed.count() << " seconds" << std::endl;

	start = std::chrono::high_resolution_clock::now();
	result = mult_threads_async_recursive(x, y);
	end = std::chrono::high_resolution_clock::now();
	elapsed = end - start;
	std::cout << "Result (async-get-recursive): " << result.get_str() << std::endl;
	std::cout << "Time taken: " << elapsed.count() << " seconds" << std::endl;

	start = std::chrono::high_resolution_clock::now();
	result = mult(x, y);
	end = std::chrono::high_resolution_clock::now();
	elapsed = end - start;
	std::cout << "Result (mult recursive): " << result.get_str() << std::endl;
	std::cout << "Time taken: " << elapsed.count() << " seconds" << std::endl;

	start = std::chrono::high_resolution_clock::now();
	result = mult_threads_join(x, y);
	end = std::chrono::high_resolution_clock::now();
	elapsed = end - start;
	std::cout << "Result (thread-join): " << result.get_str() << std::endl;
	std::cout << "Time taken: " << elapsed.count() << " seconds" << std::endl;

	start = std::chrono::high_resolution_clock::now();
	result = x*y;
	end = std::chrono::high_resolution_clock::now();
	elapsed = end - start;
	std::cout << "Result (mpz multiplication): " << result.get_str() << std::endl;
	std::cout << "Time taken: " << elapsed.count() << " seconds" << std::endl;

    return 0;
}
