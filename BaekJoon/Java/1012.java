import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.LinkedList;
import java.util.Queue;

public class Main {
    public static void main(String[] args) throws IOException {

        int[][] nextDirection = {
                { 0, 1 }, // up
                { 1, 0 }, // right
                { 0, -1 }, // down
                { -1, 0 } // left
        };

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine()); // 테스트 케이스의 개수

        for (int k = 0; k < T; k++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int M = Integer.parseInt(st.nextToken()); // 배추밭의 가로길이
            int N = Integer.parseInt(st.nextToken()); // 배추밭의 세로길이
            int K = Integer.parseInt(st.nextToken()); // 배추가 심어져 있는 위치의 개수

            int[][] map = new int[M][N];
            boolean[][] visited = new boolean[M][N];

            for (int j = 0; j < K; j++) {
                st = new StringTokenizer(br.readLine());
                int X = Integer.parseInt(st.nextToken()); // 배추의 X좌표
                int Y = Integer.parseInt(st.nextToken()); // 배추의 Y좌표

                map[X][Y] = 1;
            }

            int numWorms = 0;

            // bfs
            for (int i = 0; i < M; i++) {
                for (int j = 0; j < N; j++) {
                    if (map[i][j] == 1 && !visited[i][j]) {
                        Queue<int[]> queue = new LinkedList<>();
                        queue.offer(new int[] { i, j });
                        numWorms++;
                        visited[i][j] = true;

                        while (!queue.isEmpty()) {
                            int[] curr = queue.poll();
                            
                            int currX = curr[0];
                            int currY = curr[1];

                            for (int[] direction : nextDirection) {
                                int nextX = currX + direction[0];
                                int nextY = currY + direction[1];

                                if (nextX >= 0 && nextX < M && nextY >= 0 && nextY < N) {
                                    if (map[nextX][nextY] == 1 && !visited[nextX][nextY]) {
                                        visited[nextX][nextY] = true;

                                        queue.offer(new int[] { nextX, nextY });
                                    }
                                }
                            }
                        }
                    }
                }
            }
            System.out.println(numWorms);

        }
    }
}
