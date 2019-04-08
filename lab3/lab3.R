lab3_res = read.csv("lab3.csv")
avg_lab3_res = aggregate(Time ~ Size:Mode, data = lab3_res, FUN = mean)
avg_lab3_res$Time_Sd = aggregate(Time ~ Size:Mode, data = lab3_res, FUN = sd)$Time
plot_lab3 = ggplot(avg_lab3_res, aes(x = Size, y = Time, group = Mode)) + geom_line() + geom_errorbar(aes(ymin = Time - Time_Sd, ymax = Time + Time_Sd), width = 0.2) + labs(y="time[s]", x="size")

naive_res = avg_lab3_res[avg_lab3_res$Mode==1,]
better_res = avg_lab3_res[avg_lab3_res$Mode==2,]
blas_res = avg_lab3_res[avg_lab3_res$Mode==3,]

naive_res_y = c(naive_res["Time"])
better_res_y = c(better_res["Time"])
blas_res_y = c(blas_res["Time"])
any_res_x = c(blas_res["Size"])
res_frame = data.frame(any_res_x, naive_res_y, better_res_y, blas_res_y)
naive_fit = lm(naive_res_y ~ poly(any_res_x, 3, raw=TRUE), data=res_frame)
