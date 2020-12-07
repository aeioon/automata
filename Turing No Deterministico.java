import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class AD2P {
    ArrayList<Estados> estados = new ArrayList<>();
    ArrayList<Estados> estadosAceptados = new ArrayList<>();
    ArrayList<String> alpha = new ArrayList<>() ;
    ArrayList<String> TapeAlpha = new ArrayList<>() ;
    ArrayList<String> delta = new ArrayList<>();
    Estados initial;
    public AD2P(String filename){
        ArrayList<Estados> estados = new ArrayList<>();
        ArrayList<Estados> estadosAceptados = new ArrayList<>();
        Estados initial = null;
        String dataInitial= new String();
        ArrayList<String> alpha = new ArrayList<>() ;
        ArrayList<String> TapeAlpha = new ArrayList<>() ;
        ArrayList<String> delta = new ArrayList<>();
        try {
            File myObj = new File(filename);
            Scanner myReader = new Scanner(myObj);
            int selector=0;
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                switch (selector){
                    case 0:
                        if(data.equals("#states")){
                            selector=1;
                        }
                        break;
                    case 1:
                        if(data.equals("#initial")){
                            selector=2;
                        }
                        else{

                            estados.add(new Estados(data,new ArrayList<>()));

                        }
                        break;
                    case 2:
                        if(data.equals("#accepting")){
                            selector=3;
                        }
                        else{
                            dataInitial=data;

                        }
                        break;
                    case 3:
                        if(data.equals("inputAlphabet")){
                            selector=4;
                        }
                        else {
                            estadosAceptados.add(new Estados(data,new ArrayList<>()));
                        }
                        break;
                    case 4:
                        if(data.equals("#tapeAlphabet")){
                            selector=5;
                        }
                        else{
                            alpha.add(data);
                        }
                        break;

                    case 5:
                        if(data.equals("#transitions")){
                            selector=6;
                        }
                        else {
                            TapeAlpha.add(data);
                        }
                        break;
                    case 6:
                            delta.add(data);
                        break;

                    default:
                        System.out.println("error de selector");

                }
                initial= new Estados(dataInitial,new ArrayList<>());
                System.out.println(data);
            }
            new AD2P(estados,initial,estadosAceptados,alpha,TapeAlpha,delta);
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
    public AD2P(ArrayList<Estados> estados,Estados estadoInicial,ArrayList<Estados> estadosAceptacion,ArrayList<String> alfabetoEntrada,ArrayList<String> alfabetoCinta,ArrayList<String> Delta){
       this.estados=estados;
       this.estadosAceptados=estadosAceptacion;
       this.initial=estadoInicial;
       this.alpha = alfabetoEntrada;
       this.TapeAlpha = alfabetoCinta;
       this.delta = Delta;
    }

void crearArbol(Estados initial){
        
    }




    class Estados{
        private  String name;
        private  ArrayList<Estados> Transiciones;

        public Estados(String name, ArrayList<Estados> transiciones) {
            this.name = name;
            Transiciones = transiciones;
        }

    }
}
