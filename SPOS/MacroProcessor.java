// Design suitable data structures and implement Pass-I and Pass-II of a two-pass macro-
// processor. The output of Pass-I (MNT, MDT and intermediate code file without any macro
// definitions) should be input for Pass-II.

import java.io.*;
import java.util.*;

class MacroProcessor {
    // Macro Name Table (MNT) entry
    static class MNTEntry {
        String name;
        int mdtIndex;
        public MNTEntry(String name, int mdtIndex) {
            this.name = name;
            this.mdtIndex = mdtIndex;
        }
    }

    // Macro Definition Table (MDT) entry
    static class MDTEntry {
        String line;
        public MDTEntry(String line) {
            this.line = line;
        }
    }

    List<MNTEntry> mnt = new ArrayList<>();
    List<MDTEntry> mdt = new ArrayList<>();
    List<String> intermediate = new ArrayList<>();

    public static void main(String[] args) {
        String inputFile = "code2.asm";
        String mntFile = "mnt.txt";
        String mdtFile = "mdt.txt";
        String intermFile = "intermediate_macro.txt";
        String outputFile = "expanded_code.asm";
        MacroProcessor mp = new MacroProcessor();
        try {
            mp.pass1(inputFile, mntFile, mdtFile, intermFile);
            System.out.println("Pass-I complete. MNT, MDT, and intermediate code generated.");
            mp.pass2(intermFile, mntFile, mdtFile, outputFile);
            System.out.println("Pass-II complete. Macro expansion done. See expanded_code.asm.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Pass-I: Build MNT, MDT, and intermediate code
    public void pass1(String inputFile, String mntFile, String mdtFile, String intermFile) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(inputFile));
        String line;
        boolean inMacro = false;
        int mdtIndex = 0;
        String macroName = null;
        while ((line = br.readLine()) != null) {
            line = line.split(";")[0].trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("MACRO")) {
                inMacro = true;
                continue;
            }
            if (inMacro) {
                if (macroName == null) {
                    // Macro header: MACRO_NAME &ARG
                    String[] tokens = line.split("[ ,\t]+");
                    macroName = tokens[0];
                    mnt.add(new MNTEntry(macroName, mdtIndex));
                }
                mdt.add(new MDTEntry(line));
                mdtIndex++;
                if (line.equals("MEND")) {
                    inMacro = false;
                    macroName = null;
                }
                continue;
            }
            // Non-macro lines go to intermediate code
            intermediate.add(line);
        }
        br.close();
        // Write MNT
        BufferedWriter bw = new BufferedWriter(new FileWriter(mntFile));
        for (MNTEntry entry : mnt) {
            bw.write(entry.name + " " + entry.mdtIndex + "\n");
        }
        bw.close();
        // Write MDT
        bw = new BufferedWriter(new FileWriter(mdtFile));
        for (MDTEntry entry : mdt) {
            bw.write(entry.line + "\n");
        }
        bw.close();
        // Write intermediate code
        bw = new BufferedWriter(new FileWriter(intermFile));
        for (String s : intermediate) {
            bw.write(s + "\n");
        }
        bw.close();
    }

    // Pass-II: Expand macros using MNT and MDT
    public void pass2(String intermFile, String mntFile, String mdtFile, String outputFile) throws IOException {
        // Load MNT
        Map<String, Integer> mntMap = new HashMap<>();
        BufferedReader br = new BufferedReader(new FileReader(mntFile));
        String line;
        while ((line = br.readLine()) != null) {
            String[] tokens = line.trim().split("[ ,\t]+");
            if (tokens.length >= 2) {
                mntMap.put(tokens[0], Integer.parseInt(tokens[1]));
            }
        }
        br.close();
        // Load MDT
        List<String> mdtLines = new ArrayList<>();
        br = new BufferedReader(new FileReader(mdtFile));
        while ((line = br.readLine()) != null) {
            mdtLines.add(line);
        }
        br.close();
        // Expand macros in intermediate code
        br = new BufferedReader(new FileReader(intermFile));
        BufferedWriter bw = new BufferedWriter(new FileWriter(outputFile));
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            String[] tokens = line.split("[ ,\t]+", 2);
            String macroCall = tokens[0];
            if (mntMap.containsKey(macroCall)) {
                // Macro expansion
                int idx = mntMap.get(macroCall);
                // Find macro body in MDT
                for (int i = idx + 1; i < mdtLines.size(); i++) {
                    String macroLine = mdtLines.get(i);
                    if (macroLine.equals("MEND")) break;
                    // Replace argument if present
                    if (tokens.length > 1) {
                        macroLine = macroLine.replaceAll("&[A-Za-z0-9]+", tokens[1]);
                    }
                    bw.write(macroLine + "\n");
                }
            } else {
                bw.write(line + "\n");
            }
        }
        br.close();
        bw.close();
    }
}

