import java.util.Scanner;

abstract class PageReplacementAlgorithm {
    protected int[][] frames;
    protected int numFrames;
    protected int pageFault;
    protected int[] pages;
    protected int pagesLength;

    protected abstract void replacePage();

    public PageReplacementAlgorithm(int numFrames, int[] pages) {
        this.numFrames = numFrames;
        this.pages = pages;
        this.pagesLength = pages.length;
        this.pageFault = 0;

        this.frames = new int[pagesLength][numFrames + 1];

        // Initialize frames to -1
        for (int i = 0; i < pagesLength; i++) {
            for (int j = 0; j < numFrames + 1; j++) {
                frames[i][j] = -1;
            }
        }
    }

    protected boolean isPageFault(int index, int page) {
        for (int i = 0; i < numFrames; i++) {
            if (frames[index][i] == page) return false;
        }
        return true;
    }

    protected void copyPreviousFrame(int index) {
        if (index == 0) return;
        for (int i = 0; i < numFrames; i++) {
            frames[index][i] = frames[index - 1][i];
        }
    }

    public void displayFrames() {
        for (int i = 0; i < pagesLength; i++)
            System.out.print(pages[i] + " ");
        System.out.println("");

        for (int i = 0; i < pagesLength; i++)
            System.out.print("--");
        System.out.println("");

        for (int i = 0; i < numFrames + 1; i++) {
            for (int j = 0; j < pagesLength; j++) {
                if (frames[j][i] == -1) System.out.print("  ");
                else if (frames[j][i] == -3) System.out.print("* ");
                else System.out.print(frames[j][i] + " ");
            }
            System.out.println("");
        }

        System.out.println("\nTotal Page Hit: " + (pagesLength - pageFault));
        System.out.println("Total Page Fault: " + pageFault);
    }
}

class FIFO extends PageReplacementAlgorithm {
    private int pointer = 0;

    public FIFO(int numFrames, int[] pages) {
        super(numFrames, pages);
    }

    @Override
    protected void replacePage() {
        int page;
        for (int i = 0; i < this.pagesLength; i++) {
            page = this.pages[i];
            copyPreviousFrame(i);

            if (isPageFault(i, page)) {
                frames[i][this.pointer] = page;
                frames[i][this.numFrames] = -3; // mark page fault
                this.pointer++;
                if (this.pointer == this.numFrames) this.pointer = 0; // wrap around
                this.pageFault++;
            }
        }

        displayFrames();
    }
}


class LRU extends PageReplacementAlgorithm {
    public LRU(int numFrames, int[] pages) {
        super(numFrames, pages);
    }

    private int findLRU(int index, int[] currentFrame) {
        int lruIndex = 0;
        int minLastUsed = index;

        for (int i = 0; i < numFrames; i++) {
            int lastUsed = -1;
            for (int j = index - 1; j >= 0; j--) {
                if (currentFrame[i] == pages[j]) {
                    lastUsed = j;
                    break;
                }
            }

            if (lastUsed == -1) return i; // never used before
            else if (lastUsed < minLastUsed) {
                minLastUsed = lastUsed;
                lruIndex = i;
            }
        }

        return lruIndex;
    }

    @Override
    protected void replacePage() {
        int page;
        for (int i = 0; i < pagesLength; i++) {
            page = pages[i];
            copyPreviousFrame(i);

            if (isPageFault(i, page)) {
                // If empty slot available, fill it
                boolean placed = false;
                for (int j = 0; j < numFrames; j++) {
                    if (frames[i][j] == -1) {
                        frames[i][j] = page;
                        frames[i][numFrames] = -3;
                        pageFault++;
                        placed = true;
                        break;
                    }
                }

                // Otherwise replace the least recently used page
                if (!placed) {
                    int replaceIndex = findLRU(i, frames[i]);
                    frames[i][replaceIndex] = page;
                    frames[i][numFrames] = -3;
                    pageFault++;
                }
            }
        }
        displayFrames();
    }
}


class Optimal extends PageReplacementAlgorithm {
    public Optimal(int numFrames, int[] pages) {
        super(numFrames, pages);
    }

    private int findFurthest(int index, int[] currentFrame) {
        int pos = -1;
        int farthest = index;

        for (int i = 0; i < numFrames; i++) {
            int nextUse = -1;
            for (int j = index + 1; j < pagesLength; j++) {
                if (currentFrame[i] == pages[j]) {
                    nextUse = j;
                    break;
                }
            }

            if (nextUse == -1) {
                // Page not used again, best candidate to replace
                return i;
            } else if (nextUse > farthest) {
                farthest = nextUse;
                pos = i;
            }
        }

        // default to first if all are used soon
        return (pos == -1) ? 0 : pos; 
    }

    @Override
    public void replacePage() {
        int page;
        for (int i = 0; i < this.pagesLength; i++) {
            page = this.pages[i];
            copyPreviousFrame(i);

            if (isPageFault(i, page)) {
                // If empty slot available, fill it
                boolean placed = false;
                for (int j = 0; j < numFrames; j++) {
                    if (frames[i][j] == -1) {
                        frames[i][j] = page;
                        frames[i][numFrames] = -3;
                        this.pageFault++;
                        placed = true;
                        break;
                    }
                }

                // Otherwise replace the furthest one
                if (!placed) {
                    int replaceIndex = findFurthest(i, frames[i]);
                    frames[i][replaceIndex] = page;
                    frames[i][numFrames] = -3;
                    this.pageFault++;
                }
            }
        }
        displayFrames();
    }
}


public class PageReplacement {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the number of frames: ");
        int numFrames = scanner.nextInt();
        
        int[] pages = {1, 2, 3, 2, 1, 5, 2, 1, 6, 2, 5, 6, 3, 1, 3, 6, 1, 2, 4, 3};

        FIFO fifo = new FIFO(numFrames, pages);
        LRU lru = new LRU(numFrames, pages);
        Optimal optimal = new Optimal(numFrames, pages);
        
        
        System.out.println("\nFIFO Page Replacement:");
        fifo.replacePage();
        System.out.println("\nLRU Page Replacement:");
        lru.replacePage();
        System.out.println("\nOptimal Page Replacement:");
        optimal.replacePage();
        
        scanner.close();
    }
}  