import java.io.*;
import java.util.*;

public class Display
{
    public static void main(String[] args) throws IOException
    {
        Scanner sents = new Scanner(new File("eng-spa-align.txt"));

        Scanner align = new Scanner(new File("eng-spa-align.out"));

        int i = 0;
        while (sents.hasNextLine() && align.hasNextLine())
        {
            String[] s = sents.nextLine().split("\\|\\|\\|");
            String[] a = align.nextLine().split("\\s+");
            String[] s1 = s[0].trim().split(" ");
            String[] s2 = s[1].trim().split(" ");
            System.out.println(s[0].trim());
            System.out.println(s[1].trim());
            //System.out.println(Arrays.toString(a));

            int[] mapping = new int[s1.length];
            int[] rmapping = new int[s2.length];

            for (int x=0;x<mapping.length;++x) mapping[x] = -1;
            for (int y=0;y<rmapping.length;++y) rmapping[y] = -1;

            for (String pair : a)
            {
                String[] p = pair.split("-");
                int x = Integer.parseInt(p[0]);
                int y = Integer.parseInt(p[1]);
                //System.out.println(x + " " + s1.length);
                if (x < s1.length && y < s2.length)
                {
                    mapping[x] = y;
                    rmapping[y] = x;
                }
                else
                {
                    //System.out.println(i + " " + x + " " + y);
                    //System.exit(0);
                }
            }

            for (int x=0;x<s1.length;++x)
            {
                int y = mapping[x];
                if (y == -1) System.out.print("***" + s1[x] +  "***, ");
                else System.out.print(s1[x] + " -> " + s2[y] + ", ");
            }
            System.out.println();

            for (int y=0;y<s2.length;++y)
            {
                int x = rmapping[y];
                if (x == -1) System.out.print("***" + s2[y] +  "***, ");
                else System.out.print(s2[y] + " -> " + s1[x] + ", ");
            }
            System.out.println('\n');
        }
    }
}