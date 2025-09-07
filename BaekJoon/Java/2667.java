import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Queue;
import java.util.LinkedList;

public class Main {
    public static void main(String[] args) throws IOException {

        int[][] nextDirection = {
                { 0, 1 }, // up
                { 1, 0 }, // right
                { 0, -1 }, // down
                { -1, 0 } // left
        };

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int N = Integer.parseInt(br.readLine());
        int[][] map = new int[N][N];
        boolean[][] visited = new boolean[N][N];

        for (int i = 0; i < N; i++) {
            String line = br.readLine();
            for (int j = 0; j < N; j++) {
                map[i][j] = line.charAt(j) - '0';
            }
        }

        LinkedList<Integer> numAptList = new LinkedList<>();

        // bfs
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (map[i][j] == 1 && !visited[i][j]) {
                    Queue<int[]> queue = new LinkedList<>();
                    queue.offer(new int[] {i, j});
                    visited[i][j] = true;

                    int numApt = 0;
                    while (!queue.isEmpty()) {
                        int[] curr = queue.poll();
                        numApt++;
                        int currX = curr[0];
                        int currY = curr[1];

                        for (int[] direction : nextDirection) {
                            int nextX = currX + direction[0];
                            int nextY = currY + direction[1];

                            if (nextX >= 0 && nextX < N && nextY >= 0 && nextY < N) {
                                if (map[nextX][nextY] == 1 && !visited[nextX][nextY]) {
                                    visited[nextX][nextY] = true;
                                    
                                    queue.offer(new int[] { nextX, nextY });
                                }
                            }
                        }
                    }
                    numAptList.add(numApt);
                }
            }
        }

        numAptList.sort(null);

        System.out.println(numAptList.size());
        for (int i : numAptList) {
            System.out.println(i);
        }

    }
}
