public class l1 {
    static class SharedResource {
        private boolean active = true;

        public boolean isActive() {
            return active;
        }

        public void setActive(boolean active) {
            this.active = active;
        }
    }

    static class Worker {
        private String name;
        private boolean active;

        public Worker(String name, boolean active) {
            this.name = name;
            this.active = active;
        }

        public String getName() {
            return name;
        }

        public boolean isActive() {
            return active;
        }

        public void work(SharedResource sharedResource, Worker otherWorker) {
            while (active) {
                // Wait for the other worker to become inactive
                if (otherWorker.isActive()) {
                    System.out.println(name + " is waiting for " + otherWorker.getName() + " to become inactive.");
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    continue;
                }

                // If the shared resource is active, this worker becomes inactive and vice versa.
                if (sharedResource.isActive()) {
                    System.out.println(name + " sets the shared resource to inactive.");
                    sharedResource.setActive(false);
                } else {
                    System.out.println(name + " activates the shared resource.");
                    sharedResource.setActive(true);
                }

                // This worker becomes inactive and lets the other worker work.
                this.active = false;
                otherWorker.active = true;
            }
        }
    }

    public static void main(String[] args) {
        final SharedResource sharedResource = new SharedResource();
        final Worker worker1 = new Worker("Worker 1", true);
        final Worker worker2 = new Worker("Worker 2", true);

        new Thread(() -> worker1.work(sharedResource, worker2)).start();
        new Thread(() -> worker2.work(sharedResource, worker1)).start();
    }
}