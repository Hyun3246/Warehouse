import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.LinkedList;
import java.util.Queue;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int N = Integer.parseInt(st.nextToken());
        int M = Integer.parseInt(st.nextToken());

        int[][] maze = new int[N][M];
        for (int i = 0; i < N; i++) {
            String line = br.readLine();
            for (int j = 0; j < M; j++) {
                maze[i][j] = line.charAt(j) - '0';
            }
        }


        
        boolean visited[][] = new boolean[N][M];

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                visited[i][j] = false;
            }
        }

    
        visited[0][0] = true;

        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[] {0, 0});

        int[][] nextDirection = {
            {0, 1},  // 오른쪽
            {1, 0},  // 아래
            {0, -1}, // 왼쪽
            {-1, 0}  // 위
        };

        while (!queue.isEmpty()) {
            int[] curr = queue.poll();
            int currX = curr[0];
            int currY = curr[1];

            for (int[] direction : nextDirection) {
                int nextX = currX + direction[0];
                int nextY = currY + direction[1];

                if (nextX >= 0 && nextX < N && nextY >= 0 && nextY < M) {
                    if (maze[nextX][nextY] == 1 && !visited[nextX][nextY]) {
                        visited[nextX][nextY] = true;
                        maze[nextX][nextY] = maze[currX][currY] + 1;
                        queue.offer(new int[] {nextX, nextY});
                    }
                }
            }
            if (visited[N-1][M-1]) {
                break;
            }
        }

        System.out.println(maze[N-1][M-1]);

        // 예시 출력 (정답을 여기에 출력해야 해)
        // System.out.println(result);
    }
}
