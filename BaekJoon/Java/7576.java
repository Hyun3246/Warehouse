import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.Queue;
import java.util.LinkedList;

public class Main {

    static int[][] nextDirection = {
            { 0, 1 }, // col + 1
            { 0, -1 }, // col - 1
            { 1, 0 }, // row + 1
            { -1, 0 } // row - 1

    };

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int M = Integer.parseInt(st.nextToken());
        int N = Integer.parseInt(st.nextToken());

        int[][] box = new int[N][M];

        for (int i = 0; i < N; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < M; j++) {
                box[i][j] = Integer.parseInt(st.nextToken());
            }
        }

        Queue<int[]> ripeTomatoes = new LinkedList<>();

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                if (box[i][j] == 1) {
                    ripeTomatoes.offer(new int[] { i, j });
                }
            }
        }

        bfs(box, ripeTomatoes, N, M);

        int result = -1;
        boolean clear = true;

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                if (box[i][j]  == 0) {
                    clear = false;
                    break;
                }
                if (box[i][j] > result) {
                    result = box[i][j];
                }
            }
        }

        if (clear) {
            System.out.println(result - 1);
        }
        else {
            System.out.println(-1);
        }

    }

    private static void bfs(int[][] box, Queue<int[]> ripeTomatoes, int N, int M) {

        while (!ripeTomatoes.isEmpty()) {
            int[] curr = ripeTomatoes.poll();

            int currRow = curr[0];
            int currCol = curr[1];

            for (int[] direction : nextDirection) {
                int nextRow = currRow + direction[0];
                int nextCol = currCol + direction[1];
                if (nextRow >= 0 && nextRow < N && nextCol >= 0 && nextCol < M) {
                    if (box[nextRow][nextCol] == 0) {
                        box[nextRow][nextCol] = box[currRow][currCol] + 1;
                        ripeTomatoes.offer(new int[] { nextRow, nextCol });
                    }
                }
            }
        }
    }
}
