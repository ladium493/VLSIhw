`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/07/06 22:26:35
// Design Name: 
// Module Name: ternary
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module ternary(clk, rst, en, direct, out);
input clk,rst,en, direct;
output [1:0]out;
reg [1:0]out;
reg [1:0]state;

always @ (posedge clk or posedge rst)
begin

if(rst==1'b1)
    begin
    if(direct==1'b1)
    begin
    state=2'b00;
    out=state;
    end
    else if(direct==1'b0)
    begin
    state=2'b10;
    out=state;
    end
    end
else

begin  
case(state)
2'b00:
    begin
    if(en==1)
        begin
        if(direct==1)
            begin
            state=2'b01;
            out=state;
            end
        else
            begin
            state=2'b10;
            out=state;
            end
         end
     else
             begin
             state=2'b00;
             out=state;
             end
     end
     
2'b01:
 begin
 if(en==1)
     begin
     if(direct==1)
         begin
         state=2'b10;
         out=state;
         end
     else
         begin
         state=2'b00;
         out=state;
         end
      end
  else
          begin
          state=2'b01;
          out=state;
          end
  end
   
2'b10:
begin
if(en==1)
  begin
  if(direct==1)
      begin
      state=2'b00;
      out=state;
      end
  else
      begin
      state=2'b01;
      out=state;
      end
   end
else
    begin
    state=2'b10;
    out=state;
    end
end

endcase
end
end
endmodule
