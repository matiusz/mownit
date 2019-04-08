lab2_res = read.csv("ceesfau.csv")
vv_lab2_res = aggregate(vector.vector ~ size, data = lab2_res, FUN = mean)
vv_lab2_res$sd = aggregate(vector.vector ~ size, data = lab2_res, FUN = sd)$vector.vector
plot_vv = ggplot(vv_lab2_res, aes(size, vector.vector)) + geom_point() + geom_errorbar(aes(ymin = vector.vector - sd, ymax = vector.vector + sd), width = 0.2) + labs(y="time[s]", x="size")

vm_lab2_res = aggregate(vector.matrix ~ size, data = lab2_res, FUN = mean)
vm_lab2_res$sd = aggregate(vector.matrix ~ size, data = lab2_res, FUN = sd)$vector.matrix
plot_vm = ggplot(vm_lab2_res, aes(size, vector.matrix)) + geom_point() + geom_errorbar(aes(ymin = vector.matrix - sd, ymax = vector.matrix + sd), width = 0.2) + labs(y="time[s]", x="size")
