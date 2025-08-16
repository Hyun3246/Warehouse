import java.io.*;
import java.util.*;
import java.util.stream.*;;

public class Main {
    public static void main(String[] args) {
        // 한 줄에는 숫자, 그 다음 줄에는 숫자열
        // Scanner sc = new Scanner(System.in);
        // int n = sc.nextInt();
        // sc.nextLine();

        // String line = sc.nextLine();
        // String[] parts = line.split(" ");

        // 한 줄에 숫자 2개 공백으로 구분
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int k = sc.nextInt();

        sc.close();

        ArrayList<Integer> numbers = IntStream.rangeClosed(1, n)
                                          .boxed()
                                          .collect(Collectors.toCollection(ArrayList::new));
        
        Integer result[] = new Integer[n];

        int index = 0;

        for (int i = 0; i < n; i++) {
            index = (index + k - 1) % numbers.size();
            result[i] = numbers.get(index);
            numbers.remove(index);
        }

        StringBuilder sb = new StringBuilder();
        sb.append("<");
        for (int i = 0; i < result.length; i++) {
            sb.append(result[i]);
            if (i < result.length - 1) {
                sb.append(", ");
            }
        }
        sb.append(">");
        System.out.println(sb.toString());
    }
}
