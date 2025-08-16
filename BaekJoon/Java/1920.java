import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        sc.nextLine();

        String line = sc.nextLine();
        String[] parts = line.split(" ");

        int m = sc.nextInt();
        sc.nextLine();

        String line2 = sc.nextLine();
        String[] parts2 = line2.split(" ");

        Set<Integer> set = new HashSet<>();
        for (String p : parts) {
            set.add(Integer.parseInt(p));
        }

        for (String p: parts2) {
            int x = Integer.parseInt(p);
            System.out.println(set.contains(x) ? 1 : 0);
        }
    }
}
