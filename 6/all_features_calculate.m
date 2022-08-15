
vids = ["G:\Projects\Vids\USC#02ST6.mp4", "G:\Projects\Vids\USC#02ST7.mp4", ...        
        "G:\Projects\Vids\USC#02ST8.mp4", ...         
        "G:\Projects\Vids\USC#08ST1.mp4", "G:\Projects\Vids\USC#08ST2.mp4", ...        
        "G:\Projects\Vids\USC#08ST3.mp4", "G:\Projects\Vids\USC#08ST4.mp4", ... 
        "G:\Projects\Vids\USC#08ST5.mp4", "G:\Projects\Vids\USC#08ST6.mp4", ...
     	"G:\Projects\Vids\USC#08ST7.mp4", "G:\Projects\Vids\USC#08ST8.mp4", ...          
        "G:\Projects\Vids\USC#06ST1.mp4", "G:\Projects\Vids\USC#06ST2.mp4", ...        
        "G:\Projects\Vids\USC#06ST3.mp4", "G:\Projects\Vids\USC#06ST4.mp4", ... 
        "G:\Projects\Vids\USC#06ST5.mp4", "G:\Projects\Vids\USC#06ST6.mp4", ...
     	"G:\Projects\Vids\USC#06ST7.mp4", "G:\Projects\Vids\USC#06ST8.mp4"       
       ];
 
[~, n] = size(vids);
disp(" ");

tic
parfor (i = 1:n, 6)
  vPath = vids(i);
  mainSimpleFeatures(vPath);
end 

parfor (i = 1:n, 6)
  vPath = vids(i);    
%   mainSimpleFeatures(vPath); 
  calculateSimpleFeatures(vPath);    calculateSimple2Features(vPath); 
  calculateFixationsFeatures(vPath); calculateSpeedFeatures(vPath);    
end
toc

% shutdownToHibernate(180);

return