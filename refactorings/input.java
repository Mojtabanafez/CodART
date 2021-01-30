/* Before refactoring (Original version) */
class A
{
    public int f; /* printF , printF, */
    public int g; /* printF, printG */
    public string h; /* printH */
    public static void E(){
        print(this.g);
    }
    public static void KK(){
        print(this.g);
    }
    public static final void Test(){
        print(this.g);
    }
}
class B extends A
{
     public static void G(){
        print(this.f);
    }
}
class F extends B{
    public final static void KK(){
        print(this.f);
    }
}
class H extends F{
    public static void E(){
        print(this.f);
    }
}
/*
class C
{
    // Method 1
    final void printF(int i)
    {
        this.f = i * this.f;
    }

    // Method 2
    public static final void printF(float i){
        this.f = (int) (i * this.f);
        this.g = (int) (i * this.g);
    }

    // Method 3
    void printG(){
        print(this.g);
    }

    // Method 4
    void printH(){
        print(this.h);
    }
    // Method 5
    public static void E(int a, char c){
        print(this.g);
    }
    // Method 6
    protected void p(){
        printG();
    }
    // Method 7
    protected static void T(){
        print(this.g);
    }
    // Method 8
    protected static final void Y(){
        print(this.g);
    }
    // Method 9
    final void O(){
        print(this.g);
    }

}

*/