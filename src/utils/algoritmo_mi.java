import java.util.*;


public class Piyavski_Algorithm_next_gen implements Algorithm {

    class Intervsal implements Comparable<Interval> {
        public final double x1, x2, z1, z2, R;

        public Interval(double x1, double x2, double z1, double z2, double L) {
            this.x1 = x1;
            this.x2 = x2;
            this.z1 = z1;
            this.z2 = z2;
            // (Passo 2)
            this.R = (z1 + z2) / 2.0 - L * (x2 - x1) / 2.0;
        }

        @Override
        public int compareTo(Interval other) {
            // 1. Confronto primario: sceglie la R più piccola
            int rCompare = Double.compare(this.R, other.R);

            // 2. TIE-BREAKER: Se le R sono identiche, sceglie quello più a sinistra
            if (rCompare == 0) {
                return Double.compare(this.x1, other.x1);
            }
            return rCompare;
        }
    }


    private double a, b, L, epsilon;
    private int numIterations, maxIterations;
    private Function blackBox;
    private TreeMap<Double, Double> orderedValues = new TreeMap<>();
    private ArrayList<AbstractMap.SimpleEntry<Double, Double>> values = new ArrayList();
    private ArrayList<AbstractMap.SimpleEntry<Double, Double>> caratteristicValues = new ArrayList();
    private AlgorithmListener listener;

    Piyavski_Algorithm_next_gen() {
        this.a = 0.0;
        this.b = 0.0;
        this.epsilon = 1e-4;
    }


    public void setParameters(double a, double b, double L, double epsilon, int maxIterations, Function blackBox) {
        this.a = a;
        this.b = b;
        this.L = L;
        this.epsilon = epsilon*(b-a);
        this.maxIterations = maxIterations;
        this.blackBox = blackBox;
    }

    public void setListener(AlgorithmListener listener) {
        this.listener = listener;
    }

    public double[] run() {
        orderedValues.clear();
        numIterations = 0;
        values.clear();


        double za = blackBox.eval(a);
        double zb = blackBox.eval(b);
        orderedValues.put(a, za);
        orderedValues.put(b, zb);
        values.add(new AbstractMap.SimpleEntry<>(a, za));
        values.add(new AbstractMap.SimpleEntry<>(b, zb));

        double zStar = za;
        double xStar = a;
        if (zb < za) {
            zStar = zb;
            xStar = b;
        }

        PriorityQueue<Interval> queue = new PriorityQueue<>();
        queue.add(new Interval(a, b, za, zb, L));

        if (listener != null) {
            listener.onIteration(a, za, new TreeMap<>(orderedValues));
            listener.onIteration(b, zb, new TreeMap<>(orderedValues));
        }

        while (!queue.isEmpty()) {

            if (Thread.currentThread().isInterrupted() || numIterations+2 >= maxIterations) {
                System.out.println("Algoritmo terminato per limite iterazioni.");
                break;
            }

            try {
                Interval bestInterval = queue.poll();

                // Passo 4
                if ((bestInterval.x2 - bestInterval.x1) <= this.epsilon) {
                    System.out.println("Criterio di arresto raggiunto (ampiezza intervallo minore o uguale ad epsilon)");
                    return new double[] {xStar, zStar};
                }

                // PRUNING
                if ( zStar -bestInterval.R <= epsilon) {continue;}
                //if ( zStar  <= bestInterval.R) {continue;}


                // Passo 5
                double xNew = (bestInterval.x1 + bestInterval.x2) / 2.0 - (bestInterval.z2 - bestInterval.z1) / (2.0 * L);

                // Sicurezza numerica
                // if (orderedValues.containsKey(xNew) || xNew - bestInterval.x1 <= epsilon  || xNew - bestInterval.x2 >= -epsilon ) continue;

                double zNew = blackBox.eval(xNew);
                values.add(new AbstractMap.SimpleEntry<>(xNew, zNew));
                if (orderedValues.containsKey(xNew)) {throw new ArithmeticException("Arresto: Limite di precisione raggiunto (Punto X duplicato).");}
                orderedValues.put(xNew, zNew);

                // Aggiornamento Minimo
                if (zNew < zStar) {
                    zStar = zNew;
                    xStar = xNew;
                }

                // Aggiunta nuovi intervalli
                queue.add(new Interval(bestInterval.x1, xNew, bestInterval.z1, zNew, L));
                queue.add(new Interval(xNew, bestInterval.x2, zNew, bestInterval.z2, L));

                if (listener != null) {
                    listener.onIteration(xNew, zNew, new TreeMap<>(orderedValues));
                }

            } catch (Exception e) {
                System.out.println("Anomalia matematica rilevata all'iterazione " + numIterations + "!");
                System.out.println("Motivo: " + e.getMessage());
                return new double[] {xStar, zStar};
            }
            numIterations++;
        }

        System.out.println("Minimo trovato: f(" + xStar + ") = " + zStar);

        return new double[] {xStar,zStar};
    }

    public TreeMap<Double, Double> getOrderedValues() { return orderedValues; }

    public double getUnderestimatorValue(double x) {

        Map.Entry<Double, Double> lower = orderedValues.floorEntry(x);
        Map.Entry<Double, Double> upper = orderedValues.ceilingEntry(x);
        if (lower == null || upper == null) return Double.NaN;

        double vLeft = lower.getValue() - L * (x - lower.getKey());
        double vRight = upper.getValue() - L * (upper.getKey() - x);
        return Math.max(vLeft, vRight);
    }

    public void setA(double a) { this.a = a; }
    public void setB(double b) { this.b = b; }
    public void setL(double l) { this.L = l; }
    public void setEpsilon(double epsilon) { this.epsilon = epsilon; }

    public double getA() { return a; }
    public double getB() { return b; }
    public double getL() { return L; }
    public double getEpsilon() { return epsilon; }

    public int getNumIterations() {
        return numIterations;
    }

    public ArrayList<AbstractMap.SimpleEntry<Double, Double>> getValues() {
        return values;
    }
}