import java.io.*;
import java.util.*;

public class Alignment
{
    public static void main(String[] args) throws IOException
    {
        String lang1 = "eng";
        String lang2 = "spa";

        Scanner a = new Scanner(new File(lang1 + ".txt"));
        Scanner b = new Scanner(new File(lang2 + ".txt"));
        int line = 0;

        PrintStream out = new PrintStream(new File(lang1 + "-" + lang2 + "-align.txt"));

        while (a.hasNextLine() && b.hasNextLine())
        {
            ++line;
            String al = a.nextLine();
            String bl = b.nextLine();
            if (al.length() == 0)
            {
                al = a.nextLine();
                bl = b.nextLine();
                if (!al.equals("----------") || !bl.equals("----------"))
                {
                    System.err.println("BAD ALIGNMENT: " + line);
                    out.close();
                    return;
                }
                al = a.nextLine();
                bl = b.nextLine();
                if (!al.equals(bl))
                {
                    System.err.println("BAD ALIGNMENT: " + line);
                    out.close();
                    return;
                }
                continue;
            }

            out.println(tokenize(al) + " ||| " + tokenize(bl));
        }
    }

    public static String tokenize(String in)
    {
        String out = "";
        int type = 0;
        for (char c : in.toCharArray())
        {
            //System.out.println(c + " " + Character.isAlphabetic(c) + " " + Character.isWhitespace(c));
            if (Character.isAlphabetic(c))
            {
                if (type!=0)
                {
                    type = 0;
                    if (out.length()>0 && !Character.isWhitespace(out.charAt(out.length()-1))) out += ' ';
                }
            }
            else if (!Character.isWhitespace(c))
            {
                if (type!=1)
                {
                    type = 1;
                    if (out.length()>0 && !Character.isWhitespace(out.charAt(out.length()-1))) out += ' ';
                }
            }
            out += c;
        }
        return out;
    }
}