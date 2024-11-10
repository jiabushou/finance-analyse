股票持仓水平分析程序

CREATE TABLE `operate_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `mtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `bargain_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '成交时间',
  `bond_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '证劵代码',
  `bond_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '证劵名称',
  `operate_kind` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '操作类型(in:买入;out:卖出)',
  `bargain_number` int NOT NULL DEFAULT '0' COMMENT '成交数量(100的整数倍)',
  `bargain_unit_price` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '成交均价',
  `bargain_amount` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '成交金额',
  `contract_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '合同编号',
  `bargain_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '成交编号',
  `fee` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '手续费',
  `stamp_duty` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '印花税',
  `other_fee` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '其它杂费',
  `happen_amount` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '发生金额',
  `left_amount` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '资金余额',
  `trade_market` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '交易市场',
  `share_holder_account` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '股东账户',
  `delivery_date` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '交收日期',
  `bond_full_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '证劵中文全称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_bargain_no` (`bargain_no`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3892 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;