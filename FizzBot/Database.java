import java.io.*;
import java.util.*;

public class Database {
    public static void main(String[] args) throws IOException {
        init();
        String input[] = br.readLine().split(" ");
        if (input[0].equals("1")) {
            editUser(input[1], input[2]);
        } else if (input[0].equals("0")) {
            PrintWriter pw = new PrintWriter(new FileWriter("databaseIO.txt")); // Write query

            boolean found = false;
            for (int i = 0; i < data.size(); i++) {
                if (data.get(i).tag.equals(input[1])) {
                    pw.println(data.get(i).name);
                    pw.close();
                    found = true;
                    break;
                }
            }

            if (!found) {
                pw.println("Error: User not found");
                pw.close();
            }
        } else { // Command is 2
            PrintWriter pw = new PrintWriter(new FileWriter("databaseIO.txt")); // Write query

            boolean found = false;
            for (int i = 0; i < data.size(); i++) {
                if (data.get(i).tag.equals(input[1])) {
                    data.remove(i);
                    found = true;
                    break;
                }
            }
            if (!found) {
                pw.println("Error: User not found");
                pw.close();
            }
        }
        br.close();

        if (input[0].equals("1") || input[0].equals("2")) {
            exit();
        }
    }

    public static void init() throws IOException {
        br = new BufferedReader(new FileReader("databaseIO.txt"));
        data = new ArrayList();

        BufferedReader dataReader = new BufferedReader(new FileReader("databaseMemory.txt"));
        String input = dataReader.readLine();
        while (input != null) {
            String ind[] = input.split(" ");
            data.add(new User(ind[0], ind[1]));

            input = dataReader.readLine();
        }
    }

    public static void exit() throws IOException {
        PrintWriter pw = new PrintWriter(new FileWriter("databaseMemory.txt"));

        for (int i = 0; i < data.size(); i++) {
            pw.println(data.get(i));
        }

        pw.close();
    }

    public static void editUser(String discordTag, String username) throws IOException {
        for (int i = 0; i < data.size(); i++) {
            if (data.get(i).tag.equals(discordTag)) {
                data.get(i).setName(username);
                return;
            }
        }

        data.add(new User(discordTag, username));
    }

    private static BufferedReader br;
    private static List<User> data;

    static class User {
        String tag, name;

        User(String discordTag, String username) {
            tag = discordTag;
            name = username;
        }

        public void setName(String newName) {
            name = newName;
        }

        public String toString() {
            return tag + " " + name;
        }
    }
}