// operators/DoubleEquivalence.java
// (c)2021 MindView LLC: see Copyright.txt
// We make no guarantees that this code is fit for any purpose.
// Visit http://OnJava8.com for more book information.

public class DoubleEquivalence {
  static void show(String desc, Double n1, Double n2) {
    System.out.println(desc + ":");
    System.out.printf(
      "%e==%e %b %b%n", n1, n2, n1 == n2, n1.equals(n2));
  }
  @SuppressWarnings("deprecation")
  public static void test(double x1, double x2) {
    // x1.equals(x2) // Won't compile
    System.out.printf("%e==%e %b%n", x1, x2, x1 == x2);

    Double d1 = x1;
    Double d2 = x2;
    show("Automatic", d1, d2);

    Double r1 = new Double(x1);
    Double r2 = new Double(x2);
    show("new Double()", r1, r2);

    Double v1 = Double.valueOf(x1);
    Double v2 = Double.valueOf(x2);
    show("Double.valueOf()", v1, v2);

  }
  public static void main(String[] args) {

    //比较0和最小的浮点数
    test(0, Double.MIN_VALUE);

    System.out.println("------------------------");

    //最大值 和 （最大值 和 （最小值只差的一百万倍））比较 一个非常大的数值减去一个相对较小的数值,
    //非常大的数值并不会发生显著变化。这个叫做 <b> 舍入误差 <\b>
    test(Double.MAX_VALUE,
      Double.MAX_VALUE - Double.MIN_VALUE * 1_000_000);

    System.out.println("------------------------");
    test(2.1, 3.5);

    System.out.println("------------------------");
    System.out.println(Double.MIN_VALUE); //2^-1074
    System.out.println(Double.MAX_VALUE);


  }
}
/* Output:
0.000000e+00==4.900000e-324 false
Automatic:
0.000000e+00==4.900000e-324 false false
new Double():
0.000000e+00==4.900000e-324 false false
Double.valueOf():
0.000000e+00==4.900000e-324 false false
------------------------
1.797693e+308==1.797693e+308 true
Automatic:
1.797693e+308==1.797693e+308 false true
new Double():
1.797693e+308==1.797693e+308 false true
Double.valueOf():
1.797693e+308==1.797693e+308 false true
*/
