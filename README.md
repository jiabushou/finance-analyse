股票持仓水平分析程序

```
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
```

关系：
1. 一笔买入记录可与多笔卖出记录匹配（一次买得较多，在上涨时逐渐卖出）
2. 多笔买入记录可与一笔卖出记录匹配（上涨期间一直没卖，在较高位时一次性全部卖出）
算法：
1. 取出未匹配完的卖出记录，按时间由近到远排序
2. 遍历未匹配完的卖出记录，对于每笔卖出记录，找到与其匹配的买入记录
   a.找到与卖出记录匹配的买入记录 
      a. 取出当前卖出记录的未匹配份额，卖出时间
      b. 取出未匹配完的买入记录，按时间由近到远排序
      c. 遍历未匹配完的买入记录，找到第一笔满足如下条件的记录
         c.1. 买入时间早于买入时间
         c.2. 买入单价低于卖出单价（如果此条件不满足，则仅需满足第一个条件即可）
3. 计算匹配后的盈亏金额
      如果卖出记录单价高于买入记录单价，此匹配盈利
      盈利金额 = min(卖出记录待匹配份额，买入记录待匹配份额)*(卖出记录单价 - 买入记录单价)
      如果卖出记录单价低于买入记录单价，此匹配亏损
      亏损金额 == min(卖出记录待匹配份额，买入记录待匹配份额)*(卖出记录单价 - 买入记录单价)
4. 匹配信息更新到匹配记录表,所有卖出记录匹配完毕后，记录总亏损金额 
5. 将总亏损金额平均分摊到未匹配的买入记录的单价当中,未匹配的买入记录最新的单价信息就是当前的筹码水平
