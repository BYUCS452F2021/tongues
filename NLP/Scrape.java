import java.io.*;
import java.net.*;
import java.util.*;

public class Scrape
{
    public static void main(String[] args) throws IOException
    {
        String root = "https://abn.churchofjesuschrist.org";
        String lang = "bul";
        String add = "?lang=" + lang;

        //String next = "/study/scriptures/bofm/bofm-title";
        Scanner links = new Scanner(new File("links.txt"));
        while (links.hasNextLine())
        {
            String cur = links.nextLine();
            URL url = new URL(root + cur + add);

            Scanner in = new Scanner(url.openStream());
            String text = "";
            while (in.hasNextLine())
            {
                text += in.nextLine();
            }


            // if (text.contains("nextLink"))
            // {
            //     int index = text.indexOf("nextLink");
            //     //System.out.println(text.substring(index, index+100));
            //     index = text.indexOf("href", index) + 5;
            //     int end = text.indexOf(" ", index);
            //     next = text.substring(index, end);
            // }

            //break;

            int start = text.indexOf("<header>");
            if (start < 0) continue;
            System.out.println("----------");
            System.out.println(cur);
            int end = text.indexOf("</div>", start);
            text = text.substring(start, end);
            String[] lines = text.replaceAll("</(p|h\\d)>", "\n").replaceAll("<sup.*?</sup>", "").replaceAll("<.*?>", "").split("\n");
            for (String line : lines) System.out.println(line.strip());
            System.out.println();
        }
    }
}