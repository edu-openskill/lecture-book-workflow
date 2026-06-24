package com.metacoding.product.adapter.message;

public record ProductDecreasedEvent(int orderId, int productId, int quantity, boolean isSuccess) {}
