package com.metacoding.product.adapter.message;

public record IncreaseProductCommand(int orderId, int productId, int quantity, long price) {}
