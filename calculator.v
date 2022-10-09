module calculator(inkey, print0, print1, print2, print3);
input [3:0] inkey;
// C:1111, =:1110, +:1100

output reg [3:0] print0;
output reg [3:0] print1;
output reg [3:0] print2;
output reg [3:0] print3;
//MSB <- print3 print2 print1 print0 -> LSB
//1111=' ', 1110=E

reg [1:0] state;

//00: input the first number
//01: input the second number
//10: result
//11: keep add

reg [3:0] number10; 
reg [3:0] number11; 
reg [3:0] number12; 
reg [3:0] number13;
//MSB <- number13 number12 number11 number10 -> LSB

reg [3:0] number20;
reg [3:0] number21;
reg [3:0] number22;
reg [3:0] number23;
//MSB <- number23 number22 number21 number20 -> LSB

reg [1:0] num1use;
reg [1:0] num2use;

reg fullflag1, fullflag2, errorflag;

//add and return binary value
function [16:0] addresult ;

input [3:0] inumber10;
input [3:0] inumber11;
input [3:0] inumber12;
input [3:0] inumber13;
input [3:0] inumber20;
input [3:0] inumber21;
input [3:0] inumber22;
input [3:0] inumber23;
reg [13:0] l,r2,r3;
reg [3:0]o3;
reg [3:0]o2;
reg [3:0]o1;
reg [3:0]o0;
reg errorflag;
    begin
        l=1000*(inumber13+inumber23)+100*(inumber12+inumber22)
        +10*(inumber11+inumber21)+(inumber10+inumber20);

        o3=l/1000;
        r3=l%1000;
        o2=r3/100;
        r2=r3%100;
        o1=r2/10;
        o0=r2%10;

        if (l>9999) errorflag=1;
        else errorflag=0;

        if (errorflag) addresult=17'b11111111111111110;
        else
        begin        
        
        if (o3==0 && o2==0 && o1==0)
        begin
            o3=4'hf;
            o2=4'hf;
            o1=4'hf;
        end
        
        else if (o3==0 && o2==0)
        begin
            o3=4'hf;
            o2=4'hf;
        end
        
        else if (o3==0) o3=4'hf;

        addresult={errorflag,o3,o2,o1,o0};
        end
    end
    
endfunction

always @(inkey) begin
    if (inkey==4'b1111) begin
        //reset
        state=2'b00;
        number10=0;
        number11=0;
        number12=0;
        number13=0;

        number20=0;
        number21=0;
        number22=0;
        number23=0;

        print0=0;
        print1=4'b1111;
        print2=4'b1111;
        print3=4'b1111;

        fullflag1=0;
        fullflag2=0;
        num1use=0;
        num2use=0;
        errorflag=0;

        result=5'd0;
    end

case (state)
    2'b00:begin
        //consider about 0, +, =
        //0 in the first && =, ignore; +, turn to next state.

        if (inkey==4'b1100) begin //input +, turn to next state
        state=2'b01;
        end

        else if (!fullflag1) 
        begin
        case (num1use)
            2'b00: 
            if (inkey>4'b0000 && inkey<4'b1010) begin
                number10=inkey;
                num1use=num1use+1;
                print0=number10;
            end
                
           2'b01:
            if (inkey<4'b1010) begin
                number11=number10;
                number10=inkey;

                num1use=num1use+1;

                print0=number10;
                print1=number11;
            end

            2'b10:
            if (inkey<4'b1010) begin
                number12=number11;
                number11=number10;
                number10=inkey;

                num1use=num1use+1;

                print0=number10;
                print1=number11;
                print2=number12;
            end

            2'b11:
            if (inkey<4'b1010) begin
                number13=number12;
                number12=number11;
                number11=number10;
                number10=inkey;

                fullflag1=1;

                print0=number10;
                print1=number11;
                print2=number12;
                print3=number13;
            end
        endcase
        end
    end

    2'b01:begin
        //consider about 0, +, =
        //0 in the first, second
        //=, turn to state 11; 
        //+, turn to state 10.

        if (inkey==4'b1100) begin 
        //press + then deal it here.
        {errorflag,print3,print2,print1,print0}=addresult(number10,number11,number12,number13,number20,number21,number22,number23);
        if (errorflag) state=2'b11;
        else begin  
        number10=print0;
        if (print1==4'b1111) number11=0;
        else number11=print1;
        if (print2==4'b1111) number12=0;
        else number12=print2;
        if (print3==4'b1111) number13=0;
        else number13=print3;

        number20=0;
        number21=0;
        number22=0;
        number23=0;

        fullflag1=0;
        fullflag2=0;
        num1use=0;
        num2use=0;   
        end    
        end
        
        else if (inkey==4'b1110) begin //=
        state=2'b10;
        {errorflag,print3,print2,print1,print0}=addresult(number10,number11,number12,number13,number20,number21,number22,number23);
        if (errorflag) state=2'b11;
        else begin 
        number20=0;
        number21=0;
        number22=0;
        number23=0;

        fullflag1=0;
        fullflag2=0;
        num1use=0;
        num2use=0; 
        end
        end

        else begin

        case (num2use)
            
            2'b00: 
            if (inkey<4'b1010) begin
                number20=inkey;
                num2use=num2use+1;
                print0=number20;
                print1=4'b1111;
                print2=4'b1111;
                print3=4'b1111;
            end
                
            2'b01:
            if (inkey<4'b1010) begin
                if (!(inkey==0 && number20==0)) begin
                number21=number20;
                number20=inkey;

                num2use=num2use+1;

                print0=number20;
                print1=number21;                   
                end

            end

            2'b10:
            if (inkey<4'b1010) begin
                number22=number21;
                number21=number20;
                number20=inkey;

                num2use=num2use+1;

                print0=number20;
                print1=number21;
                print2=number22;
            end

            2'b11:
            if (inkey<4'b1010) begin
                number23=number22;
                number22=number21;
                number21=number20;
                number20=inkey;

                fullflag2=1;

                print0=number20;
                print1=number21;
                print2=number22;
                print3=number23;
            end

        endcase
        end
    end

    10:begin //=
        if (inkey==4'b1100)//+
        begin
        number10=print0;
        if (print1==4'b1111) number11=0;
        else number11=print1;
        if (print2==4'b1111) number12=0;
        else number12=print2;
        if (print3==4'b1111) number13=0;
        else number13=print3;

        number20=0;
        number21=0;
        number22=0;
        number23=0;

        fullflag1=0;
        fullflag2=0;
        num1use=0;
        num2use=0;  
        end

        else if (inkey<4'b1100)//number
        begin
            number10=0;
            number11=0;
            number12=0;
            number13=0;

            number10=inkey;
            num1use=1;
            state=2'b00;

            print0=number10;
            print1=4'b1111;
            print2=4'b1111;
            print3=4'b1111;
        end

    end     

    11:begin
    ; //error
    end 
endcase
end
endmodule