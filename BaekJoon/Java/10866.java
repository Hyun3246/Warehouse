import java.io.*;
import java.util.*;
import java.util.stream.*;;

public class Main {
    public static void main(String[] args) {
        // 한 줄에는 숫자, 그 다음 줄에는 숫자열
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();


        LinkedList<Integer> arr = new LinkedList<>();

        for (int i = 0; i < n; i++) {
            String s = sc.next();

            switch (s) {
                case "push_front":
                    int m1 = sc.nextInt();
                    push_front(arr, m1);
                    break;
                case "push_back":
                    int m2 = sc.nextInt();
                    push_back(arr, m2);
                    break;
                case "pop_front":
                    System.out.println(pop_front(arr));
                    break;
                case "pop_back":
                    System.out.println(pop_back(arr));
                    break;
                case "size":
                    System.out.println(size(arr));
                    break;
                case "empty":
                    System.out.println(empty(arr) ? 1 : 0);
                    break;
                case "front":
                    System.out.println(front(arr));
                    break;
                case "back":
                    System.out.println(back(arr));
                    break;
            }
        }

        sc.close();
    }

    public static void push_front(LinkedList<Integer> arr, int value) {
        arr.addFirst(value);
    }

    public static void push_back(LinkedList<Integer> arr, int value) {
        arr.addLast(value);
    }

    public static int pop_front(LinkedList<Integer> arr) {
        return arr.isEmpty() ? -1 : arr.removeFirst();
    }

    public static int pop_back(LinkedList<Integer> arr) {
        return arr.isEmpty() ? -1 : arr.removeLast();
    }

    public static int size(LinkedList<Integer> arr) {
        return arr.size();
    }

    public static boolean empty(LinkedList<Integer> arr) {
        return arr.isEmpty();
    }

    public static int front(LinkedList<Integer> arr) {
        return arr.isEmpty() ? -1 : arr.getFirst();
    }

    public static int back(LinkedList<Integer> arr) {
        return arr.isEmpty() ? -1 : arr.getLast();
    }
}
