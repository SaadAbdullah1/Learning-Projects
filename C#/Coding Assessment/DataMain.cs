using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Coding_Assessment
{
    class CsvMain
    {
        static void Main(string[] args)
        {
            CSVData data = new CSVData();
            data.loadDataTable();

            int quantity = data.totalQuantitySold();
            Console.WriteLine("The total quantity sold is " + quantity + " products." + Environment.NewLine);

            double totalRevenue = data.overallRevenue();
            Console.WriteLine("The total revenue of all products is $" + totalRevenue + "." + Environment.NewLine);

            //display the perProduct array
            int counter = 0;
            foreach (var product in data.totalRevenuePerProduct())
            {
                Console.WriteLine("Total revenue of Product #" + data.getID()[counter] + " is $" + product);
                counter++;
            }

            int popularID = data.mostPopularID();
            int popular = data.mostPopularProduct();
            Console.WriteLine(Environment.NewLine + "The most popular product based on quantity sold, is Product #" + popularID + " which is sold " + popular + " times.");
           
            //print off the data metrics in results.txt
            String fullPath = @"C:\Users\Me\Desktop\Student Developer\results.txt";
            int count = 0;
            using (StreamWriter writer = new StreamWriter(fullPath))
            {
                writer.WriteLine("The total quantity sold is " + quantity + " products." + Environment.NewLine);
                writer.WriteLine("The total revenue of all products is $" + totalRevenue + "." + Environment.NewLine);
                foreach (var product in data.totalRevenuePerProduct())
                {
                    writer.WriteLine("Total revenue of Product #" + data.getID()[count] + " is $" + product);
                }
                writer.WriteLine(Environment.NewLine + "The most popular product based on quantity sold, is Product #" + popularID + " which is sold " + popular + " times.");
            }
        }

    }
}
