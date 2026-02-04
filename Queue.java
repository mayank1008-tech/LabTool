class Queue {
    static final int size = 10;
    static int[] queue = new int[size];
    static int front = -1;
    static int rear = -1;

    static void enqueue(int data) {
        if (rear == size - 1) {
            System.out.println("Queue is Full");
            return;
        }
        if (front == -1) {
            front = 0;
        }
        queue[++rear] = data;
        System.out.println(data + " inserted");
    }

    static void dequeue() {
        if (front == -1 || front > rear) {
            System.out.println("Queue is Empty");
            return;
        }
        System.out.println(queue[front] + " removed");
        front++;
    }

    static void display() {
        if (front == -1 || front > rear) {
            System.out.println("Queue is Empty");
            return;
        }
        System.out.print("Queue elements: ");
        for (int i = front; i <= rear; i++) {
            System.out.print(queue[i] + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        enqueue(10);
        enqueue(20);
        enqueue(30);
        display();

        dequeue();
        display();
    }
}
