using System;
using System.Collections.Generic;
using System.Data;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Security;
using System.Security.Cryptography.X509Certificates;
using System.Security.Permissions;
using LumenWorks.Framework.IO.Csv;

namespace Coding_Assessment
{
    class CSVData
    {
        List<CSVData> searchParameters = new List<CSVData>();

        public string productId { get; set; } //first data column
        public string quantity { get; set; }  //second data column
        public string unitPrice { get; set; } //third data column
        public string saleTime { get; set; }  //fourth data column
        
        public void loadDataTable()
        {
            //loads data into the data table from data.csv
            var csvTable = new DataTable();
            using (var csvReader = new CsvReader(new StreamReader(File.OpenRead(@"C:\Users\Me\Desktop\Student Developer\data.csv")), true))
            {
                csvTable.Load(csvReader);
            }

            //add each row to the list, with their respective property binding
            for (int i = 0; i < csvTable.Rows.Count; i++)
            {
                searchParameters.Add(new CSVData
                {
                    productId = csvTable.Rows[i][0].ToString(),
                    quantity = csvTable.Rows[i][1].ToString(),
                    unitPrice = csvTable.Rows[i][2].ToString(),
                    saleTime = csvTable.Rows[i][3].ToString()
                });
            }
        }

        public int totalQuantitySold()
        {
            int quantitySold = 0;
            foreach(var product in searchParameters)
            {
                //cast to an int
                quantitySold += Int32.Parse(product.quantity);                
            }
            return quantitySold;
        }

        public List<double> totalRevenuePerProduct()
        {
            //an array to store the individual product revenue
            List<double> perProduct = new List<double>();
            double unitRevenue = 0;
            int quantity = 0;

            foreach (var product in searchParameters)
            {
                quantity = Int32.Parse(product.quantity);
                double price = Convert.ToDouble(product.unitPrice);
                unitRevenue =  quantity * price;
                perProduct.Add(unitRevenue);
            }
            return perProduct;
        }
        
        //a getter for the productID
        public List<string> getID()
        {
            List<string> idList = new List<string>();
            foreach (var i in searchParameters)
            {
                //add each product id from column to the list index'
                idList.Add(i.productId);
            }
            return idList;
        }

        //most popular product on the basis of quantity sold
        public int mostPopularProduct()
        {
            List<int> sorted = new List<int>();

            foreach(var x in searchParameters)
            {
                sorted.Add(Int32.Parse(x.quantity));
            }

            return sorted.Max();
        }

        public int mostPopularID()
        {
            int popular = 0;
            int q = 0;

            foreach (var x in searchParameters)
            {
                q = Int32.Parse(x.quantity);

                //looks through the quantity column, to match a value with the max value product calculated above
                if (q.CompareTo(mostPopularProduct()) == 0)
                {
                    //if matched, stores the productID at that quantity location in this var
                    popular = Int32.Parse(x.productId);
                }
            }
            return popular;
        }

        public double overallRevenue()
        {
            double totalRevenue = 0;
            foreach (var product in searchParameters)
            {
                //cast to an int
                int unit = Int32.Parse(product.quantity);
                double price = Convert.ToDouble(product.unitPrice);
                totalRevenue += unit * price;
            }
                return totalRevenue;
        }

        public void highestRevenueMonth()
        {
            /*this function should return the month of each saleTime row
             * in a foreach loop, in unison with the totalRevenuePerProduct() method's return value
             * then, take the value of each dateTime.month and 
             * 
             */
            int qHolder = 0;
            int revenue = 0;
            int totalRevenue = 0;

            foreach (var s in searchParameters)
            {
                DateTime dt = DateTime.ParseExact(s.saleTime, "yyyy-MM-dd HH:mm", CultureInfo.InvariantCulture);
                qHolder = Int32.Parse(s.quantity);

                switch (dt.Month)
                {
                    case 6:
                        foreach(var i in totalRevenuePerProduct())
                        {
                           // Console.WriteLine(i);
                        }

                       // Console.WriteLine("This is the month of June");
                        break;
                    case 7:
                        //Console.WriteLine("This is the month of July");
                        break;
                    case 8:
                        //Console.WriteLine("This is the month of August");
                        break;
                    case 9:
                        //Console.WriteLine("This is the month of September");
                        break;
                    case 10:
                       // Console.WriteLine("This is the month of October");
                        break;
                }
            }

        }

    }
}
