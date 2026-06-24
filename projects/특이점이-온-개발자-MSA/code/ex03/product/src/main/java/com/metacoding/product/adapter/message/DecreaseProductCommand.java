package com.metacoding.product.adapter.message;

public record DecreaseProductCommand(int orderId, int productId, int quantity, long price) {}
