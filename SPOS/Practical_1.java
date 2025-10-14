// Practical_1.java
// Pass-I and Pass-II of a simple two-pass assembler
// Produces: intermediate.txt, symbol_table.txt, literal_table.txt, machine_code.txt

import java.io.*;
import java.util.*;
import java.util.regex.*;

class Practical_1 {
    static class Symbol {
        String name;
        Integer address;
        Symbol(String name, Integer address) {
            this.name = name;
            this.address = address;
        }
    }
    static class Literal {
        String value;
        Integer address;
        Literal(String value, Integer address) {
            this.value = value;
            this.address = address;
        }
    }

    public static void main(String[] args) throws IOException {
        String inputFile = args.length > 0 ? args[0] : "code.asm";
        String symFile = args.length > 1 ? args[1] : "symbol_table.txt";
        String litFile = args.length > 2 ? args[2] : "literal_table.txt";
        String intermFile = args.length > 3 ? args[3] : "intermediate.txt";
        pass1(inputFile, symFile, litFile, intermFile);
        pass2(intermFile, symFile, litFile, "machine_code.txt");
    }

    static void pass1(String inputFile, String symFile, String litFile, String intermFile) throws IOException {
        Map<String, Integer> IS = Map.of("MOVER", 4, "ADD", 1, "SUB", 2, "MULT", 3, "MOVEM", 5, "BC", 7);
        Map<String, Integer> AD = Map.of("START", 1, "END", 2);
        Map<String, Integer> DL = Map.of("DS", 1, "DC", 2);
        Map<String, Integer> REG = Map.of("AREG", 1, "BREG", 2, "CREG", 3, "DREG", 4);

        Map<String, Integer> symbolIndex = new LinkedHashMap<>();
        Map<String, Integer> symbolTable = new LinkedHashMap<>();
        Map<String, Integer> literalIndex = new LinkedHashMap<>();
        Map<String, Integer> literalTable = new LinkedHashMap<>();
        List<String> literalPool = new ArrayList<>();
        List<String> intermediate = new ArrayList<>();
        int loc = 0;

        List<String> lines = readAssemblyFile(inputFile);
        for (String line : lines) {
            String[] tokens = line.split("[ ,\t]+");
            if (tokens.length == 0 || tokens[0].isEmpty()) continue;
            String label = null;
            if (!IS.containsKey(tokens[0]) && !AD.containsKey(tokens[0]) && !DL.containsKey(tokens[0])) {
                label = tokens[0];
                tokens = Arrays.copyOfRange(tokens, 1, tokens.length);
                if (tokens.length == 0) {
                    symbolIndex.putIfAbsent(label, symbolIndex.size() + 1);
                    symbolTable.put(label, loc);
                    continue;
                }
            }
            if (tokens.length == 0) continue;
            String opcode = tokens[0];
            if (AD.containsKey(opcode)) {
                if (opcode.equals("START")) {
                    String val = tokens.length > 1 ? tokens[1] : "0";
                    try { loc = Integer.parseInt(val); } catch (Exception e) { loc = 0; }
                    intermediate.add("(AD, " + AD.get(opcode) + ") (C, " + val + ")");
                } else if (opcode.equals("END")) {
                    intermediate.add("(AD, " + AD.get(opcode) + ")");
                    for (String lit : literalPool) {
                        if (!literalTable.containsKey(lit) || literalTable.get(lit) == null) {
                            literalTable.put(lit, loc);
                            loc++;
                        }
                    }
                }
                continue;
            }
            if (label != null) {
                symbolIndex.putIfAbsent(label, symbolIndex.size() + 1);
                symbolTable.put(label, loc);
            }
            if (IS.containsKey(opcode)) {
                int opCode = IS.get(opcode);
                String regCode = "00";
                String operand = null;
                if (tokens.length > 1 && REG.containsKey(tokens[1])) {
                    regCode = String.format("%02d", REG.get(tokens[1]));
                    if (tokens.length > 2) operand = tokens[2];
                } else if (tokens.length > 1) {
                    operand = tokens[1];
                }
                String rgPart = "(RG, " + regCode + ")";
                String isPart = "(IS, " + String.format("%02d", opCode) + ")";
                if (operand == null) {
                    intermediate.add(isPart + " " + rgPart);
                } else if (operand.startsWith("='") && operand.endsWith("'")) {
                    String lit = operand;
                    if (!literalIndex.containsKey(lit)) {
                        literalIndex.put(lit, literalIndex.size() + 1);
                        literalPool.add(lit);
                        literalTable.put(lit, null);
                    }
                    intermediate.add(isPart + " " + rgPart + " (L, " + literalIndex.get(lit) + ")");
                } else if (operand.matches("\\d+")) {
                    intermediate.add(isPart + " " + rgPart + " (C, " + operand + ")");
                } else {
                    String sym = operand;
                    if (!symbolIndex.containsKey(sym)) {
                        symbolIndex.put(sym, symbolIndex.size() + 1);
                        symbolTable.put(sym, null);
                    }
                    intermediate.add(isPart + " " + rgPart + " (S, " + symbolIndex.get(sym) + ")");
                }
                loc++;
            } else if (DL.containsKey(opcode)) {
                int dlCode = DL.get(opcode);
                String val = tokens.length > 1 ? tokens[1] : "0";
                intermediate.add("(DL, " + String.format("%02d", dlCode) + ") (C, " + val + ")");
                if (opcode.equals("DC")) loc++;
                else if (opcode.equals("DS")) {
                    try { loc += Integer.parseInt(val); } catch (Exception e) {}
                }
            }
        }
        // Write symbol table
        List<String> symLines = new ArrayList<>();
        for (String name : symbolIndex.keySet()) {
            Integer addr = symbolTable.get(name);
            symLines.add(name + " " + (addr != null ? addr : "-"));
        }
        List<String> litLines = new ArrayList<>();
        for (String lit : literalIndex.keySet()) {
            Integer addr = literalTable.get(lit);
            litLines.add(lit + " " + (addr != null ? addr : "-"));
        }
        writeLines(symFile, symLines);
        writeLines(litFile, litLines);
        writeLines(intermFile, intermediate);
        System.out.println("Pass-1 complete. Wrote " + intermFile + ", " + symFile + ", " + litFile + ".");
    }

    static void pass2(String intermFile, String symFile, String litFile, String outFile) throws IOException {
        List<Integer> symAddrs = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(symFile))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(" ");
                if (parts.length < 2) continue;
                String addr = parts[1];
                symAddrs.add(addr.equals("-") ? null : Integer.parseInt(addr));
            }
        }
        List<Integer> litAddrs = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(litFile))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(" ");
                if (parts.length < 2) continue;
                String addr = parts[1];
                litAddrs.add(addr.equals("-") ? null : Integer.parseInt(addr));
            }
        }
        Map<String, String> DL = Map.of("DS", "01", "DC", "02");
        List<String> machineLines = new ArrayList<>();
        int loc = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(intermFile))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                List<String> parts = new ArrayList<>();
                Matcher m = Pattern.compile("\\(([^)]+)\\)").matcher(line);
                while (m.find()) parts.add(m.group(1).trim());
                String isField = parts.stream().filter(p -> p.startsWith("IS,")).findFirst().orElse(null);
                String adField = parts.stream().filter(p -> p.startsWith("AD,")).findFirst().orElse(null);
                String dlField = parts.stream().filter(p -> p.startsWith("DL,")).findFirst().orElse(null);
                String rgField = parts.stream().filter(p -> p.startsWith("RG,")).findFirst().orElse(null);
                String opcode = "00", rg = "00"; int addr = 0;
                if (adField != null) {
                    String[] adParts = adField.split(",", 2);
                    String code = adParts.length > 1 ? adParts[1].trim() : "";
                    String cfield = parts.stream().filter(p -> p.startsWith("C,")).findFirst().orElse(null);
                    if (cfield != null && code.equals("01")) {
                        try { loc = Integer.parseInt(cfield.split(",", 2)[1].trim()); } catch (Exception e) { loc = 0; }
                    }
                    continue;
                }
                if (isField != null) {
                    opcode = isField.split(",", 2)[1].trim();
                    if (rgField != null) rg = rgField.split(",", 2)[1].trim();
                    String operand = parts.stream().filter(p -> p.startsWith("L,") || p.startsWith("S,") || p.startsWith("C,")).findFirst().orElse(null);
                    if (operand != null) {
                        String[] opParts = operand.split(",", 2);
                        String kind = opParts[0].trim();
                        String val = opParts[1].trim();
                        if (kind.equals("L")) {
                            int idx = Integer.parseInt(val) - 1;
                            addr = (idx >= 0 && idx < litAddrs.size() && litAddrs.get(idx) != null) ? litAddrs.get(idx) : 0;
                        } else if (kind.equals("S")) {
                            int idx = Integer.parseInt(val) - 1;
                            addr = (idx >= 0 && idx < symAddrs.size() && symAddrs.get(idx) != null) ? symAddrs.get(idx) : 0;
                        } else if (kind.equals("C")) {
                            addr = Integer.parseInt(val);
                        }
                    }
                    machineLines.add(opcode + " " + rg + " " + addr);
                    loc++;
                } else if (dlField != null) {
                    String dlCode = dlField.split(",", 2)[1].trim();
                    String cfield = parts.stream().filter(p -> p.startsWith("C,")).findFirst().orElse(null);
                    int constVal = cfield != null ? Integer.parseInt(cfield.split(",", 2)[1].trim()) : 0;
                    machineLines.add(dlCode + " 00 " + loc);
                    if (dlCode.equals(DL.get("DC"))) loc++;
                    else {
                        try { loc += constVal; } catch (Exception e) {}
                    }
                }
            }
        }
        writeLines(outFile, machineLines);
        System.out.println("Pass-2 complete. Wrote " + outFile + " (" + machineLines.size() + " lines).");
    }

    static List<String> readAssemblyFile(String filename) throws IOException {
        List<String> lines = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String raw;
            while ((raw = br.readLine()) != null) {
                String line = raw.split(";")[0].trim();
                if (!line.isEmpty()) lines.add(line);
            }
        }
        return lines;
    }

    static void writeLines(String filename, List<String> lines) throws IOException {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(filename))) {
            for (String l : lines) bw.write(l + "\n");
        }
    }
}
