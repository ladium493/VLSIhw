module passma(clk,rst,pass,led);
input clk,rst;
input [3:0]pass;

output [3:0]led;

reg [3:0]led;
reg [3:0]para1;
reg [3:0]para2;
//para2->para1
reg [2:0]progress;
// key: 0111, 1100, 0010, 1110

always @(posedge clk or posedge rst) begin
    if (rst==1'b1)
    begin
        para1=4'b0000;
        para2=4'b0000;
        progress=3'b000;
        led=4'b0000;
    end
    else
    begin
    para1=para2;
    para2=pass;
    
    case (progress)
        3'b000:
        begin
            if (para1== 4'b0111 && para2==4'b0000)
            begin
            progress=3'b001;
            led=4'b0001;
            end
        end

        3'b001:
        begin
            if (para1== 4'b1100 && para2==4'b0000)
            begin
            progress=3'b010;
            led=4'b0011;
            end
        end

        3'b010:
        begin
            if (para1== 4'b0010 && para2==4'b0000)
            begin
            progress=3'b011;
            led=4'b0111;
            end
        end       

        3'b011:
        begin
            if (para1== 4'b1110 && para2==4'b0000)
            begin
            led=4'b1111;
            end
        end
    
    endcase
    end
end

endmodule