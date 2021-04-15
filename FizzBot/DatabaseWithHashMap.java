import java.io.*;
import java.util.*;

public class DatabaseWithHashMap {
    public static void main(String[] args) throws IOException {
        init();
        String input[] = br.readLine().split(" ");
        if (input[0].equals("1")) {
            editUser(input[2], input[1]);
        } else if (input[0].equals("0")) {
            PrintWriter pw = new PrintWriter(new FileWriter("databaseIO.txt")); // Write query
            pw.println(data.getOrDefault(input[1], "Error"));
        } else { // Command is 2
            PrintWriter pw = new PrintWriter(new FileWriter("databaseIO.txt")); // Write query
            if (!data.containsKey(input[1])) {
                pw.println("Error");
                pw.close();
            } else {
                data.remove(input[1]);
            }
        }
        br.close();

        if (input[0].equals("1") || input[0].equals("2")) {
            exit();
        }
    }

    public static void init() throws IOException {
        br = new BufferedReader(new FileReader("databaseIO.txt"));
        data = new HashMap<String, String>();

        BufferedReader dataReader = new BufferedReader(new FileReader("databaseMemory.txt"));
        String input = dataReader.readLine();
        while (input != null && input.length() > 0) {
            String ind[] = input.split(" ");
            data.put(ind[0], ind[1]);

            input = dataReader.readLine();
        }
    }

    public static void exit() throws IOException {
        PrintWriter pw = new PrintWriter("databaseMemory.txt");
        for (Map.Entry e : data.entrySet()) {
            pw.println((String) e.getKey() + " " + (String) e.getValue());
        }
        pw.close();
    }

    public static void editUser(String discordTag, String username) throws IOException {
        data.put(discordTag, username);
    }

    private static BufferedReader br;
    private static Map<String, String> data;

}