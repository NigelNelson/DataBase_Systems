/**
 * @author Aparna Joshi
 *
 * Updated 10/04/2021, update 9/29/2018
 * JDBC example to demonstrate how to connect,
 * create a statement, issue a query, and process a results
 * set.
 *
 */

import java.sql.*;

public class TestJDBCCopy {
    public static void main(String[] args) {
        try {
            TestJDBCCopy j = new TestJDBCCopy();
            String countryCode = "USA";

            String query = "SELECT * FROM country WHERE code ='"+ countryCode+"'";

            Connection connect = DriverManager.getConnection("jdbc:mysql://localhost:3306/world_db",
                    "root","root");
            Statement stmt = connect.createStatement();
            ResultSet rs = stmt.executeQuery(query);
			//need to use executeUpdate method for update queries

            while(rs.next()) {
                System.out.println("country code:"+ rs.getString(1));
                System.out.println("country name:"+ rs.getString(2));
                System.out.println("continent :"+ rs.getString(3));
                System.out.println("surface area:"+ rs.getString(5));
            }

        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }

    }

}
