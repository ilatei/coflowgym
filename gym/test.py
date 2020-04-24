import matplotlib.pyplot as plt
import numpy as np

from analyse import plot_compare, validate_reward
from benchdata import exp4_benchmark_data

def analyse_test():
    result, ep_r = exp4_benchmark_data()
    result = [53006632.0, 133996904.0, 79770400.0, 46296840.0, 63063464.0, 71356176.0, 46305232.0, 24366896.0, 27429784.0, 25094768.0, 27732944.0, 28246712.0, 25745304.0, 27572200.0, 27774528.0, 32610376.0, 30800280.0, 27115224.0, 29090832.0, 32548160.0, 36948384.0, 40699584.0, 35654928.0, 36650192.0, 36285440.0, 33193856.0, 37559104.0, 47884168.0, 33104856.0, 34441560.0, 33294120.0, 31723328.0, 31744624.0, 30031280.0, 35635200.0, 28001744.0, 27450176.0, 36361216.0, 55416376.0, 54569544.0, 80998768.0, 47885016.0, 36912504.0, 36214424.0, 30277904.0, 35018824.0, 31912120.0, 31682600.0, 29777128.0, 36058024.0, 34526448.0, 27657560.0, 31144016.0, 28672512.0, 32548928.0, 33948952.0, 35544024.0, 30460312.0, 37806160.0, 37522960.0, 36478648.0, 39045928.0, 30126072.0, 32675688.0, 44710768.0, 31735392.0, 39052232.0, 63123632.0, 37536424.0, 53652304.0, 29443600.0, 30357664.0, 30573776.0, 37158408.0, 34620944.0, 33067496.0, 34484816.0, 39617568.0, 46159632.0, 41858776.0, 35639024.0, 36720192.0, 35461456.0, 37079552.0, 36534224.0, 36671696.0, 48812960.0, 37560792.0, 50255664.0, 41138984.0, 40630552.0, 45832968.0, 43689264.0, 80095720.0, 49616296.0, 37589000.0, 41506280.0, 38834360.0, 46310200.0, 36832728.0, 70105416.0, 44614160.0, 34511248.0, 29612752.0, 26422328.0, 31761304.0, 28460776.0, 38407376.0, 36654168.0, 39189544.0, 39482792.0, 46295640.0, 35809912.0, 36687688.0, 32787584.0, 45618288.0, 37210312.0, 31492360.0, 39996232.0, 34165336.0, 30430136.0, 39858048.0, 34136248.0, 33590712.0, 37502432.0, 37134360.0, 40199856.0, 84376520.0, 44615760.0, 31432296.0, 41380608.0, 31238336.0, 35172512.0, 33685280.0, 34865688.0, 34426312.0, 34649144.0, 38520376.0, 33940048.0, 34953040.0, 34073184.0, 33740472.0, 35690176.0, 36701752.0, 36490392.0, 33862752.0, 35087664.0, 34891008.0, 33958416.0, 31507888.0, 34628208.0, 35000480.0, 34630232.0, 31921040.0, 35126648.0, 32753288.0, 33103528.0, 45339344.0, 35529120.0, 33652160.0, 35240312.0, 35388280.0, 39858392.0, 36802960.0, 39999160.0, 39857832.0, 45608216.0, 38830728.0, 38084624.0, 29361960.0, 33163752.0, 33305104.0, 39635888.0, 38133208.0, 33257696.0, 36303000.0, 35621488.0, 40677672.0, 40538688.0, 30019432.0, 35669464.0, 40011208.0, 46900176.0, 37826760.0, 40814352.0, 45430080.0, 46887712.0, 44590560.0, 39618816.0, 68297984.0, 37520448.0, 39342240.0, 46681776.0, 41341368.0, 43485608.0, 44366840.0, 41966520.0, 33915264.0, 42041672.0, 48033768.0, 45089056.0, 44103944.0, 45911296.0, 45062928.0, 56534352.0, 49214776.0, 42056808.0, 49158512.0, 45961256.0, 39732944.0, 37661856.0, 46034448.0, 34916808.0, 42114872.0, 40659496.0, 40332688.0, 40530440.0, 39974232.0, 42215976.0, 42657976.0, 56616496.0, 44863848.0, 42429424.0, 40752576.0, 41353192.0, 44803032.0, 33523376.0, 41948400.0, 30740048.0, 29554512.0, 34350912.0, 31646376.0, 30028176.0, 35595584.0, 30999264.0, 30917656.0, 30718744.0, 28045560.0, 32335240.0, 32769072.0, 32712032.0, 36035720.0, 34087120.0, 34602408.0, 33438552.0, 36044512.0, 31461632.0, 33578944.0, 34367088.0, 43987496.0, 38373056.0, 34582552.0, 40476120.0, 39082968.0, 32938080.0, 31803288.0, 33071728.0, 35175600.0, 33046808.0, 32945336.0, 32768840.0, 40785552.0, 45565288.0, 44535408.0, 39529968.0, 35455984.0, 38844992.0, 34318456.0, 36399656.0, 37192920.0, 35740576.0, 39955680.0, 41120752.0, 80641400.0, 42425936.0, 44815280.0, 58716224.0, 49763248.0, 38626744.0, 39681624.0, 46734144.0, 45642728.0, 54708552.0, 43621392.0, 44537808.0, 43466368.0, 42672368.0, 42290872.0, 39576664.0, 42415008.0, 40673032.0, 43436976.0, 43188464.0, 43618440.0, 44628304.0, 45145800.0]





    ep_r = [-8001.187840657781, -17429.63013903688, -12046.109207861642, -7753.648657926886, -10245.267743984703, -11351.289756162918, -7132.560066210747, -4463.109695558151, -5690.546882992426, -5079.670610968109, -5729.352331035231, -5422.424743768445, -4968.673954957114, -5736.651552167044, -5841.214676231011, -6741.06463596854, -5414.581579802721, -4890.787947730557, -5229.951977259027, -6402.069824008851, -7271.8830784845095, -7133.1161678686285, -6995.448657106702, -6402.1583851143, -6497.259521078721, -6046.591404554005, -6887.004117046239, -7416.9888459461945, -4779.660845279529, -5572.217073600467, -6004.563307583643, -6039.40749991862, -6034.303171142145, -5923.961745869243, -11864.01399343234, -5217.200515787594, -6353.1438458484345, -5772.686582635963, -9074.882831372865, -8830.36923404454, -12671.378423918528, -7397.414888821719, -6116.4129408699955, -6956.4585532588, -6228.737076012854, -6995.967709568128, -6464.995639862487, -6261.34410364938, -6335.48184677392, -7429.275000819794, -6135.789096247444, -5097.365874360545, -6515.44030200016, -5826.948085297542, -5356.999112281666, -5274.865854459746, -5599.241141853442, -5021.852832551764, -6317.847046037379, -6035.998571529058, -5850.538107143318, -6406.682281148416, -4458.814320908801, -5867.0344637497965, -7211.023231750063, -5089.894597153687, -6558.970756970801, -10380.976797659396, -5684.599265450773, -8050.355145792509, -4557.488487604337, -4627.452867875178, -4739.4409042042935, -6077.772983131115, -5947.506943190609, -5266.200584582507, -5696.822407446271, -6236.8943212765125, -7222.437659206437, -6472.5490618489275, -5753.163755541954, -5407.474977502553, -5687.331297832403, -6165.9695220597805, -6243.60343153435, -5992.764257049104, -8438.241490576138, -6200.236821397369, -8779.721291934908, -6730.132356160055, -6828.553540064779, -7990.683277461157, -7743.737509291759, -12207.371286037393, -8475.718509328302, -6488.843800987251, -7146.509594731782, -6512.542031034412, -7903.000231640441, -6211.418499573745, -11848.068659129769, -6544.715754606086, -5443.13267464082, -5112.726615289881, -4234.147928614291, -5275.069160103908, -4511.189325866932, -6358.09213133895, -6030.68152768555, -6424.003183055984, -6505.209552183611, -7863.52672615051, -5704.341603948278, -5878.020620435072, -5394.45505123723, -6903.94694714453, -5752.263491335996, -4719.8187595479585, -6562.089684632385, -5493.305493544887, -5099.496852383626, -6765.598472608786, -5612.2787864899, -5112.950888948649, -6258.162160666546, -6000.194329974115, -6640.304200909085, -13243.150986956065, -7095.672714391441, -4868.441990443899, -6389.2344558431605, -5062.891117617108, -5769.388777418497, -5444.270890726708, -5598.071770652899, -5534.330646042954, -5472.940525294175, -6198.40960623948, -5570.439750977351, -5725.554524181503, -5628.685971730405, -5556.5827138730965, -5562.525157951859, -5989.374542378038, -6045.962086663796, -5562.060178599663, -5738.096261091414, -5604.152331611109, -5581.473650948142, -5057.316842390176, -5929.520409318845, -6106.522578393705, -6058.665568428949, -5557.180833379156, -5699.468939214835, -5660.927940123304, -5442.84648018643, -7267.6727257184, -5681.985392260717, -5411.92920391079, -5641.254670732526, -5531.585507696579, -6464.367077004484, -5858.77080134086, -6359.1848450036005, -6456.154640168869, -7150.0130816890605, -6111.011093008824, -6314.686395859608, -5049.933836682654, -5370.251652894006, -5836.944279651154, -6516.112063677141, -6268.903360358185, -5427.659897361511, -5848.645769340362, -5842.007794679612, -6715.773595231212, -6969.4063307197175, -5100.528012173245, -5878.386391690297, -7065.856254527653, -7696.599248688437, -6384.194030053954, -7208.332858609236, -7400.124934509724, -7605.383090264668, -7561.787713669032, -6549.089548403656, -11340.590029588657, -5955.808545426198, -6255.77240814357, -7320.148021108491, -6659.620965960292, -6926.75645614485, -7117.375132462914, -6783.636331353524, -5426.593583831347, -6872.743523386196, -7682.304483343006, -7189.506163153456, -7115.602164824269, -7542.412183384457, -7059.772474738425, -8569.490270171647, -7900.8433362990545, -6645.782814162307, -7746.620287908492, -7393.9554586213735, -6335.483358005582, -6146.300928804261, -7353.585167943106, -5607.743173321517, -6518.977477237225, -6471.008029727556, -6321.400236491697, -6371.893545101792, -6208.82011486163, -6617.072581247973, -6582.053868862256, -8913.263536262499, -6816.056364150164, -6795.625779241086, -6669.024660598613, -6616.383835679921, -7238.147277450664, -5187.095238457232, -6764.092542285413, -4817.947040506837, -4774.142395830579, -5476.273284401521, -4595.4387289812, -4599.809846473836, -5961.686248322715, -5176.88564549041, -5803.850351665121, -5809.367578635755, -6614.717532857304, -6240.56730474184, -6040.415788689443, -5756.513900762509, -6865.707004821013, -5750.311631793117, -6605.981747608296, -6289.083295929072, -6798.475781893727, -5613.794952571913, -6333.91169151344, -5589.306872472711, -7316.922191097433, -5724.931049696047, -6319.052762394552, -7112.069520933768, -7034.981440778018, -5850.264638973414, -6042.520510298846, -6417.743300488565, -6815.219754671327, -6326.708708650524, -5388.216679903704, -5387.594391870999, -6637.871447089186, -7226.858115604581, -7049.417892882125, -6352.58130096531, -5938.220217337697, -6137.807408864535, -5885.846679990744, -6074.196739432937, -6371.1374124544645, -5714.93010730566, -6561.121337111942, -6696.032228951386, -12993.049603017478, -6903.076270776273, -7077.166645069166, -9002.330214513422, -7879.370105401666, -6183.129823947494, -6317.814964942859, -7571.574479953878, -7294.994536401018, -8749.136726647544, -7044.214623174193, -7132.150255180043, -6950.485790554537, -6884.551719066723, -6893.049514432336, -6414.118184781952, -6800.628552276476, -6511.563774489349, -6890.671508317481, -6892.027836959081, -7044.311109231429, -7105.234664725973, -7079.584634405701]




    print("Number of samples:", len(result))
    validate_reward(result, ep_r)
    plot_compare(result, ep_r)
    plt.show()

def f():
    a = np.arange(10)
    b = a+np.random.randn(10,)
    plt.scatter(a, b)

    z = np.poly1d(np.polyfit(a, b, 1))
    c = z(a)
    plt.plot(a, c)

    plt.show()
    

if __name__ == "__main__":
    pass
    analyse_test()
    # f()