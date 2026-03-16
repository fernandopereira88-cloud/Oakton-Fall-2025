/*
 * Author: Ivan Temesvari
 * Date: 5/21/2024
 * This is a dynamic divide-and-conquer parallel multiplication algorithm.
 * This program uses parallel schemes for concurrency to compute
 * the product of large integers.
 * 
 */
import java.math.BigInteger;
import java.util.concurrent.*;

public class ParallelMultiplication {
	
	 static class MultiplyTask implements Runnable {
        BigInteger x;
        BigInteger y;
        BigInteger result; // Instance variable to store the result

        MultiplyTask(BigInteger x, BigInteger y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public void run() {
            result = multRunnable(x, y); // Compute the result
        }
    }

    static BigInteger multRunnable(BigInteger x, BigInteger y) {
        int len_x = x.toString().length();
        int len_y = y.toString().length();
        if (x.compareTo(BigInteger.TEN) == -1 || y.compareTo(BigInteger.TEN) == -1) {
            return x.multiply(y);
        } else {
            BigInteger x1 = x.divide(BigInteger.TEN.pow(len_x / 2));
            BigInteger x2 = x.mod(BigInteger.TEN.pow(len_x / 2));
            BigInteger y1 = y.divide(BigInteger.TEN.pow(len_y / 2));
            BigInteger y2 = y.mod(BigInteger.TEN.pow(len_y / 2));

            ExecutorService executor = Executors.newFixedThreadPool(8);
            MultiplyTask[] tasks = new MultiplyTask[4];
            tasks[0] = new MultiplyTask(x1, y1);
            tasks[1] = new MultiplyTask(x1, y2);
            tasks[2] = new MultiplyTask(x2, y2);
            tasks[3] = new MultiplyTask(y1, x2);

            for (MultiplyTask task : tasks) {
                executor.execute(task); // Submit tasks to the executor
            }

            executor.shutdown();
            try {
                executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            // Calculate the final result using the partial results from tasks
            BigInteger P1 = tasks[0].result;
            BigInteger P2 = tasks[1].result;
            BigInteger P3 = tasks[2].result;
            BigInteger P4 = tasks[3].result;

            BigInteger pow1 = BigInteger.TEN.pow(len_x / 2 + len_y / 2);
            BigInteger pow2 = BigInteger.TEN.pow(len_x / 2);
            BigInteger pow3 = BigInteger.TEN.pow(len_y / 2);

            return P1.multiply(pow1)
                    .add(P2.multiply(pow2))
                    .add(P3)
                    .add(P4.multiply(pow3));
        }
    }
	
	static BigInteger mult_threads_recursive(BigInteger x, BigInteger y) {
        int len_x = String.valueOf(x).length();
        int len_y = String.valueOf(y).length();
        if (x.compareTo(BigInteger.TEN) == -1 || y.compareTo(BigInteger.TEN) == -1) {
            return x.multiply(y);
        } else {
            BigInteger x1 = x.divide(BigInteger.TEN.pow(len_x / 2));
            BigInteger x2 = x.mod(BigInteger.TEN.pow(len_x / 2));
            BigInteger y1 = y.divide(BigInteger.TEN.pow(len_y / 2));
            BigInteger y2 = y.mod(BigInteger.TEN.pow(len_y / 2));

            ExecutorService executor = Executors.newFixedThreadPool(8);
            Callable<BigInteger> task1 = () -> mult_threads(x1, y1);
            Callable<BigInteger> task2 = () -> mult_threads(x1, y2);
            Callable<BigInteger> task3 = () -> mult_threads(x2, y2);
            Callable<BigInteger> task4 = () -> mult_threads(y1, x2);

            BigInteger P1 = BigInteger.ZERO;
            BigInteger P2 = BigInteger.ZERO;
            BigInteger P3 = BigInteger.ZERO;
            BigInteger P4 = BigInteger.ZERO;
            try {
                Future<BigInteger> future1 = executor.submit(task1);
                Future<BigInteger> future2 = executor.submit(task2);
                Future<BigInteger> future3 = executor.submit(task3);
                Future<BigInteger> future4 = executor.submit(task4);

                P1 = future1.get();
                P2 = future2.get();
                P3 = future3.get();
                P4 = future4.get();
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
            executor.shutdown();

            BigInteger pow1 = BigInteger.TEN.pow(len_x / 2 + len_y / 2);
            BigInteger pow2 = BigInteger.TEN.pow(len_x / 2);
            BigInteger pow3 = BigInteger.TEN.pow(len_y / 2);

            return P1.multiply(pow1)
                    .add(P2.multiply(pow2))
                    .add(P3)
                    .add(P4.multiply(pow3));
        }
	}
	
	static BigInteger mult_threads(BigInteger x, BigInteger y) {
        int len_x = String.valueOf(x).length();
        int len_y = String.valueOf(y).length();
        if (x.compareTo(BigInteger.TEN) == -1 || y.compareTo(BigInteger.TEN) == -1) {
            return x.multiply(y);
        } else {
            BigInteger x1 = x.divide(BigInteger.TEN.pow(len_x / 2));
            BigInteger x2 = x.mod(BigInteger.TEN.pow(len_x / 2));
            BigInteger y1 = y.divide(BigInteger.TEN.pow(len_y / 2));
            BigInteger y2 = y.mod(BigInteger.TEN.pow(len_y / 2));

            ExecutorService executor = Executors.newFixedThreadPool(8);
            Callable<BigInteger> task1 = () -> mult(x1, y1);
            Callable<BigInteger> task2 = () -> mult(x1, y2);
            Callable<BigInteger> task3 = () -> mult(x2, y2);
            Callable<BigInteger> task4 = () -> mult(y1, x2);

            BigInteger P1 = BigInteger.ZERO;
            BigInteger P2 = BigInteger.ZERO;
            BigInteger P3 = BigInteger.ZERO;
            BigInteger P4 = BigInteger.ZERO;
            try {
                Future<BigInteger> future1 = executor.submit(task1);
                Future<BigInteger> future2 = executor.submit(task2);
                Future<BigInteger> future3 = executor.submit(task3);
                Future<BigInteger> future4 = executor.submit(task4);

                P1 = future1.get();
                P2 = future2.get();
                P3 = future3.get();
                P4 = future4.get();
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
            executor.shutdown();

            BigInteger pow1 = BigInteger.TEN.pow(len_x / 2 + len_y / 2);
            BigInteger pow2 = BigInteger.TEN.pow(len_x / 2);
            BigInteger pow3 = BigInteger.TEN.pow(len_y / 2);

            return P1.multiply(pow1)
                    .add(P2.multiply(pow2))
                    .add(P3)
                    .add(P4.multiply(pow3));
        }
	}
	
    static BigInteger mult(BigInteger x, BigInteger y) {
        int len_x = x.toString().length();
        int len_y = y.toString().length();
        if (x.compareTo(BigInteger.TEN) == -1 || y.compareTo(BigInteger.TEN) == -1) {
            return x.multiply(y);
        } else {
            BigInteger[] xDivMod = x.divideAndRemainder(BigInteger.TEN.pow(len_x / 2));
            BigInteger x1 = xDivMod[0];
            BigInteger x2 = xDivMod[1];

            BigInteger[] yDivMod = y.divideAndRemainder(BigInteger.TEN.pow(len_y / 2));
            BigInteger y1 = yDivMod[0];
            BigInteger y2 = yDivMod[1];

            BigInteger P1 = mult(x1, y1).multiply(BigInteger.TEN.pow((len_x / 2) + (len_y / 2)));
            BigInteger P2 = mult(x1, y2).multiply(BigInteger.TEN.pow(len_x / 2));
            BigInteger P3 = mult(x2, y2);
            BigInteger P4 = mult(y1, x2).multiply(BigInteger.TEN.pow(len_y / 2));

            return P1.add(P2).add(P3).add(P4);
        }
    }

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        BigInteger x = new BigInteger("9248723412123456124343243245325566545454358769219834539434523453426435");
        BigInteger y = new BigInteger("6924126745567865434326657889774555534984502495486004038899837498372495");
        
        long startTime = System.nanoTime();
        BigInteger result = multRunnable(x, y);
        long endTime = System.nanoTime();
        double executionTime = (endTime - startTime) / 1e9;
        System.out.println("Execution time (parallel recursive threads with runnable): " + executionTime + " seconds");
        System.out.println(result);
        
        startTime = System.nanoTime();
        result = mult_threads_recursive(x, y);
        endTime = System.nanoTime();
        executionTime = (endTime - startTime) / 1e9;
        System.out.println("Execution time (parallel recursive threads with callable): " + executionTime + " seconds");
        System.out.println(result);
        
        startTime = System.nanoTime();
        result = mult_threads(x, y);
        endTime = System.nanoTime();
        executionTime = (endTime - startTime) / 1e9;
        System.out.println("Execution time (parallel non-recursive threads with callable): " + executionTime + " seconds");
        System.out.println(result);

        startTime = System.nanoTime();
        result = mult(x, y);
        endTime = System.nanoTime();
        executionTime = (endTime - startTime) / 1e9;
        System.out.println("Execution time (non-parallel recursive): " + executionTime + " seconds");
        System.out.println(result);

        startTime = System.nanoTime();
        result = x.multiply(y);
        endTime = System.nanoTime();
        executionTime = (endTime - startTime) / 1e9;
        System.out.println("Execution time (built-in): " + executionTime + " seconds");
        System.out.println(result);
    }
}
