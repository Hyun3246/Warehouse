import java.io.*;
import java.util.*;

public class Main {
    static int count = 0;
    static int result = -1;
    static int K;
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        StringTokenizer st;

        String[] input = br.readLine().split(" ");
        int N = Integer.parseInt(input[0]);
        K = Integer.parseInt(input[1]);


        st = new StringTokenizer(br.readLine());
        int[] arr = new int[N];
        for (int i = 0; i < N; i++) {
            arr[i] = Integer.parseInt(st.nextToken());
        }


        mergeSort(arr, 0, N-1);

        bw.write(result + "\n");


        bw.flush();
        bw.close();
        br.close();
    }

    public static void mergeSort(int[] arr, int left, int right) {
        if (left < right) {
            int mid = (left + right) / 2;
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            merge(arr, left, mid, right);
        }
    }

    public static void merge(int[] arr, int left, int mid, int right){
        int i = left;
        int j = mid+1;
        int t = 0;
        int[] tmp = new int[right - left + 1];

        while (i <= mid && j <= right){
            if (arr[i] <= arr[j]){
                tmp[t++] = arr[i++];
            }
            else {
                tmp[t++] = arr[j++];
            }
        }
        while (i <= mid) {
            tmp[t++] = arr[i++];
        }
        while (j <= right) {
            tmp[t++] = arr[j++];
        }    

        i = left;
        t = 0;
        while (i <= right) {
            count++;
            if (count == K) {
                result = tmp[t];
            }
            arr[i++] = tmp[t++];
        }
    }
}
