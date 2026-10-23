from figs import crop
jobs=[('deeab7f9','8.(','9.(','fig_n4_8.png'),
('deeab7f9','9.(','10.(','fig_n4_9.png'),
('deeab7f9','10.(','11.(','fig_n4_10.png'),
('4998d149','14.(','15.(','fig_k4_14.png'),
('82d479d1','()(2)小韓','2.請閱讀','fig_h6_g2.png'),
('nan6','7.(','8.(','fig_n6_7.png'),
('nan6','9.(','10.(','fig_n6_9.png'),
('kang6','1.(','2.(','fig_k6_1.png'),
('kang6','8.(','9.(','fig_k6_8.png'),
('kang6','11.(','12.(','fig_k6_11.png')]
for j in jobs: print(j[3],crop(*j))
