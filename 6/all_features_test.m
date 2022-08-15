SS = ["22ST1", "22ST2", "22ST3", "22ST4", "22ST5", "22ST6", ...
      "12ST1", "12ST2", "12ST3", "12ST4", "12ST5", "12ST6",  "12ST7", "12ST8", ...
      "13ST3", "13ST4", "13ST5", "13ST6", "13ST8"];
       
for i = 1:19
    S = SS(i);
    test_metrics_speed(S, 1);
    test_metrics_speed(S, 2);
    test_metrics_speed(S, 3);
    test_metrics_speed(S, 4);
end


for i = 1:19
    S = SS(i);
    test_metrics_fixsations(S, 1);
    test_metrics_fixsations(S, 2);
end

for i = 1:19
    S = SS(i);
    test_metrics_gaze(S, 1);
    test_metrics_gaze(S, 2);
end

for i = 1:19
    S = SS(i);
    test_metrics_head(S, 1);
    test_metrics_head(S, 2);
end

disp('Done');