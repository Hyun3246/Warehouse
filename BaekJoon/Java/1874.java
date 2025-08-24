import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class Main {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int n = Integer.parseInt(br.readLine());
        Integer[] arr = new Integer[n];
        Integer[] numbers = new Integer[n];

        Stack<Integer> stack = new Stack<>();

        for (int i = 0; i < n; i++) {
            int value = Integer.parseInt(br.readLine());
            arr[i] = value;
            numbers[i] = value;
        }
        Arrays.sort(numbers);

        
        int counter = 0;        // 배열에서의 포인터

        for (Integer num : numbers) {
            if (num.equals(arr[counter])) {
                sb.append("+\n");
                sb.append("-\n");
                counter++;
                while (!stack.isEmpty() && counter < n && stack.peek().equals(arr[counter])) {
                    stack.pop();
                    sb.append("-\n");
                    counter++;
                }
            }
            else {
                while (!stack.isEmpty() && counter < n && stack.peek().equals(arr[counter])) {
                    stack.pop();
                    sb.append("-\n");
                    counter++;
                }
                stack.push(num);
                sb.append("+\n");
            }
        }

        if (counter == n) {
            System.out.println(sb.toString());
        } else {
            System.out.println("NO");
        }
        } 
        
    }
